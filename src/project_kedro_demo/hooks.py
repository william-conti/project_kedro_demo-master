"""Project hooks."""
from typing import Any, Dict, Iterable, Optional

from kedro.config import ConfigLoader
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.versioning import Journal
from kedro.pipeline import Pipeline
from kedro.config import TemplatedConfigLoader
from kedro.pipeline import Pipeline
from kedro.config import TemplatedConfigLoader
from voyager.kedro_glass.core.pipelines import (
    _get_config_pipelines,
    _get_nodes_config,
    _get_pipelines_config,
)

class ProjectHooks:
    @hook_impl
    def register_pipelines(self) -> Dict[str, Pipeline]:
        """Registers the pipelines with the KedroContext.

        These pipelines are created dynamically based on configuration files
        containing pipelne and node definitions.

        Returns:
            A dictionary of Kedro Pipelines.
        """
        pipelines_config = _get_pipelines_config(self.config_loader)
        nodes_config = _get_nodes_config(self.config_loader, nodes_pattern="**/nodes/*")
        return _get_config_pipelines(pipelines_config, nodes_config)

    @hook_impl
    def register_config_loader(
            self, conf_paths: Iterable[str], env: str, extra_params: Dict[str, Any],
    ) -> ConfigLoader:
        # Templated Config
        self.config_loader = TemplatedConfigLoader(  # pylint: disable=attribute-defined-outside-init  # noqa: E501
            conf_paths,
            globals_pattern="*globals.yml",  # read the globals dictionary from project config
            globals_dict={},
        )
        return self.config_loader

    @hook_impl
    def register_catalog(
        self,
        catalog: Optional[Dict[str, Dict[str, Any]]],
        credentials: Dict[str, Dict[str, Any]],
        load_versions: Dict[str, str],
        save_version: str,
        journal: Journal,
    ) -> DataCatalog:
        return DataCatalog.from_config(
            catalog, credentials, load_versions, save_version, journal
        )
