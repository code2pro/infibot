import logging


def get_logger(log_category):
    '''Return logger with specified log category'''
    FORMAT = '%(asctime)s.%(msecs)03d:%(process)d:%(thread)d %(name)s %(levelname)s %(filename)s:%(lineno)d: %(message)s'
    DATE_FORMAT = '%Y-%m-%d_%H:%M:%S'
    formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(log_category)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
