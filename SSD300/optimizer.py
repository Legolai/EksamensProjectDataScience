import torch
from torch import optim
import math


class DemonAdam(optim.Optimizer):

    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), epochs=100,
                 eps=1e-8, weight_decay=0, nus=(0.7, 1.0), k=0.5, alpha=0.5,
                 gamma=1e-3, use_gc=True, use_grad_noise=False, step_per_epoch=None):
        if not 0.0 <= lr:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if not 0.0 <= eps:
            raise ValueError("Invalid epsilon value: {}".format(eps))
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError(
                "Invalid beta parameter at index 0: {}".format(betas[0]))
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError(
                "Invalid beta parameter at index 1: {}".format(betas[1]))
        if not 0.0 <= betas[2] < 1.0:
            raise ValueError(
                "Invalid beta parameter at index 2: {}".format(betas[2]))
        if not 0.0 <= nus[0] <= 1.0:
            raise ValueError(
                "Invalid nu parameter at index 0: {}".format(nus[0]))
        if not 0.0 <= nus[1] <= 1.0:
            raise ValueError(
                "Invalid nu parameter at index 1: {}".format(nus[1]))
        if not 0.0 <= alpha <= 1.0:
            raise ValueError("Invalid alpha parameter: {}".format(alpha))

        self.use_gc = use_gc
        self.use_grad_noise = use_grad_noise
        self.k = k
        self.epochs = epochs
        # self.IA_cycle = IA_cycle
        # self.IA = IA
        self.step_per_epoch = step_per_epoch
        self.T = self.epochs*self.step_per_epoch
        defaults = dict(lr=lr,
                        betas=betas,
                        nus=nus,
                        eps=eps,
                        alpha=alpha,
                        gamma=gamma,
                        weight_decay=weight_decay)

        super(DemonAdam, self).__init__(params, defaults)

    def __setstate__(self, state):
        super(DemonAdam, self).__setstate__(state)

    def step(self, activate_IA=False, closure=None):
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad.data.float()
                if grad.is_sparse:
                    raise RuntimeError(
                        'DemonRanger does not support sparse gradients')

                state = self.state[p]

                if len(state) == 0:
                    state['step'] = 0
                    state['exp_avg'] = torch.zeros_like(p.data)
                    state['exp_avg_sq'] = torch.zeros_like(p.data)
                    state['num_models'] = 0
                    state['cached_params'] = p.data.clone()

                state['step'] += 1
                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                beta1_init, beta2, beta3 = group['betas']
                nu1, nu2 = group['nus']
                lr = group['lr']
                wd = group['weight_decay']
                gamma = group['gamma']

                temp = 1-(state['step']/self.T)
                beta1 = beta1_init * temp / \
                    ((1-beta1_init)+beta1_init*temp)

                if self.use_grad_noise:
                    grad_var = lr/((1+state['step'])**gamma)
                    grad_noise = torch.empty_like(grad).normal_(
                        mean=0.0, std=math.sqrt(grad_var))
                    grad.add_(grad_noise)

                if self.use_gc and grad.view(-1).size(0) > 1:
                    grad.add_(-grad.mean(dim=tuple(range(1,
                              len(list(grad.size())))), keepdim=True))

                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)
                exp_avg.mul_(beta1).add_(grad, alpha=1-beta1)

                momentum = exp_avg.clone()
                momentum.div_(
                    1 - (beta1 ** state['step'])).mul_(nu1).add_(grad, alpha=1-nu1)

                if wd != 0:
                    p.data.add_(p.data, alpha=-wd*lr)

                beta2_t = beta2 ** state['step']

                vt = exp_avg_sq.clone()

                bias_correction2 = 1 - beta2_t
                vt.div_(bias_correction2)
                if nu2 != 1.0:
                    vt.mul_(nu2).addcmul_(grad, grad, value=1 - nu2)
                denom = vt.sqrt_().add_(group['eps'])
                n = lr/denom

                p.data.add_(-n*momentum)

        return loss
