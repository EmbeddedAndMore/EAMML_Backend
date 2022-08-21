from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf


def load_config():
    initialize(config_path=".", version_base=None)
    cfg: DictConfig = compose(config_name="config")
    print("config:", cfg)
    return cfg
