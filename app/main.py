from fastapi.middleware.cors import CORSMiddleware
import fsspec
import xarray as xr
import cf_xarray
import xpublish

# from xpublish.routers import base_router, zarr_router

# from xpublish_edr.cf_edr_router import cf_edr_router
# from xpublish_edr.plugin import CfEdrPlugin
# from xpublish_opendap import dap_router


# ww3 = xr.open_dataset("../restful-grids/datasets/ww3_72_east_coast_2022041112.nc")

# mapper = fsspec.get_mapper(
#     "https://ioos-code-sprint-2022.s3.amazonaws.com/gfs-wave.zarr"
# )
# gfs = xr.open_zarr(mapper, consolidated=True)


# datasets = {"ww3": ww3 } #, "gfs": gfs, "gfs5": gfs}
datasets = {}


class TestDatasetPlugin(xpublish.Plugin):
    name: str = "test-dataset-provider"

    @xpublish.hookimpl
    def get_catalogs(self):
        return ["ww3"]

    @xpublish.hookimpl
    def get_datasets(self):
        return ["ww3", "air", "example_temp"]

    @xpublish.hookimpl
    def get_dataset(self, dataset_id: str):
        if dataset_id == "ww3":
            return ww3
        if dataset_id == "air":
            return xr.tutorial.open_dataset("air_temperature")
        if dataset_id == "example_temp":
            return xr.open_dataset("./xpublish_example/average_temp.json", engine="kerchunk")
        
        return None

# rest = xpublish.SingleDatasetRest(ww3,
rest = xpublish.Rest(datasets,
    routers=[
    #     (base_router, {"tags": ["info"]}),
        # (cf_edr_router, {"tags": ["edr"], "prefix": "/edr"}),
    #     # (tree_router, {"tags": ["datatree"], "prefix": "/tree"}),
        # (dap_router, {"tags": ["opendap"], "prefix": "/opendap"}),
    #     # (tile_router, {"tags": ["image"], "prefix": "/tile"}),
    #     # (wms_router, {"tags": ["wms"], "prefix": "/wms"}),
    #     (zarr_router, {"tags": ["zarr"], "prefix": "/zarr"}),
    ],
    # plugin_configs={
    #     # "cf_edr": {
    #     #     "dataset_router_prefix": "/cf_edr_test_override"
    #     # }
    # },
    # extend_plugins={
    #     "cf_edr": CfEdrPlugin(dataset_router_prefix="/cf_edr_extended")
    # },
    # exclude_plugin_names=["module_version"]
)

rest.register_plugin(TestDatasetPlugin())

from xpublish_intake_provider import IntakeDatasetProviderPlugin

rest.register_plugin(
    IntakeDatasetProviderPlugin(
        name="gfs-datasets",
        uri="https://raw.githubusercontent.com/axiom-data-science/mc-goods/main/mc_goods/gfs-1-4deg.yaml"
    )
)
rest.register_plugin(
    IntakeDatasetProviderPlugin(
        name="gomofs-datasets",
        uri="https://raw.githubusercontent.com/axiom-data-science/mc-goods/main/mc_goods/gomofs.yaml"
    )
)



app = rest.app

app.description = "Hacking on xpublish during the IOOS Code Sprint"
app.title = "IOOS xpublish"

edr_description = """
OGC Environmental Data Retrieval API
Currently the position query is supported, which takes a single Well Known Text point.
"""

app.openapi_tags = [
    {"name": "info"},
    {
        "name": "edr",
        "description": edr_description,
        "externalDocs": {
            "description": "OGC EDR Reference",
            "url": "https://ogcapi.ogc.org/edr/",
        },
    },
    # {"name": "image", "description": "WMS-like image generation"},
    # {"name": "datatree", "description": datatree_description},
    # {"name": "opendap", "description": "OpenDAP access"},
    # {"name": "zarr", "description": zarr_description},
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    # When run directly, run in debug mode
    uvicorn.run(
        "main:app", 
        port=9005, 
        reload=True, 
        log_level="debug", 
        # debug=True
    )
