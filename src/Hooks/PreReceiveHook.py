"""
Base Hook for pre-receive treatment.
Similar to Update instead that it is executed one for
every branch pushed when update is executed one by branch
if pre-receive fails nothing is updated

AUTHOR:
    Gael Magnan de bornier
"""

from src.Hooks.ExchangeHook import ExchangeHook

class PreReceiveHook(ExchangeHook):
    """
    Base Hook for pre-receive treatment.
    Similar to Update instead that it is executed one for
    every branch pushed when update is executed one by branch
    if pre-receive fails nothing is updated
    """

    pass
