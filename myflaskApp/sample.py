import logging
import employee

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('sample.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

def add(x, y):
    #"""Add Function"""
    return x + y


def subtract(x, y):
    #"""Subtract Function"""
    return x - y


def multiply(x, y):
    #"""Multiply Function"""
    return x * y


def divide(x, y):
    #"""Divide Function"""
    try:
        result = x / y
    except ZeroDivisionError:
        logger.exception('Tried to divide by zero')
    else:
return result

logger.debug('Add: {} + {} = {}'.format(num_1, num_2, add_result))