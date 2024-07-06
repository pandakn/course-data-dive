import logging


def setup_logger(name: str = __name__, level: int = logging.INFO):
	formatter = logging.Formatter(
		'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)

	return logger


logger = setup_logger()
