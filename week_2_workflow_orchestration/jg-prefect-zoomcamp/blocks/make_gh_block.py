
from prefect import GitHub

gh_block = GitHub(
    name = 'de-zoom', repository = "https://github.com/jagord24/DataEngineeringZoomcamp"
)

gh_block.save('de-zoom', overwrite=True)