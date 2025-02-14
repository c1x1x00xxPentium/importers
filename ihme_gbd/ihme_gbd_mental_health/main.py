"""Executes bulk dataset import + chart updates for the IHME GBD mental health dataset.

The download step is fairly manual and needs some setting up before running. More details in download.py.

Usage:
    python -m ihme_gbd.ihme_gbd_mental_health.main

    python -m ihme_gbd.ihme_gbd_mental_health.main --skip_download --skip_clean
"""
from turtle import up
import click
import re
from ihme_gbd.ihme_gbd_mental_health import (
    CONFIGPATH,
    DATASET_DIR,
    DATASET_NAMESPACE,
    FILTER_FIELDS,
    INPATH,
    NAMESPACE,
    OUTPATH,
    CLEAN_ALL_VARIABLES,
    UPDATE_EXISTING_DATA_VERSION,
)

from ihme_gbd.ihme_gbd_mental_health import download, clean
from ihme_gbd import match_variables, init_variables_to_clean

from standard_importer import import_dataset
from standard_importer.chart_revision_suggester import ChartRevisionSuggester


@click.command()
@click.option(
    "--download_data/--skip_download",
    default=True,
    help="Whether or not to download the data from the source as it often takes quite some time.",
)
@click.option(
    "--clean_data/--skip_clean",
    default=True,
    help="Whether or not to clean the data, useful for just upserting previously cleaned data",
)
@click.option(
    "--import_data/--skip_import",
    default=True,
    help="Whether or not to import the data",
)
def main(download_data, clean_data, import_data):
    if download_data:
        download.main()
    if not CLEAN_ALL_VARIABLES:
        init_variables_to_clean.main(
            configpath=CONFIGPATH,
            inpath=INPATH,
            outpath=OUTPATH,
            namespace=NAMESPACE,
            fields=FILTER_FIELDS,
            update_existing_data=UPDATE_EXISTING_DATA_VERSION,
        )
    if clean_data:
        clean.main()
    if import_data:
        import_dataset.main(
            dataset_dir=DATASET_DIR, dataset_namespace=DATASET_NAMESPACE
        )
    match_variables.main(outpath=OUTPATH, namespace=re.sub("ihme_", "", NAMESPACE))

    suggester = ChartRevisionSuggester(DATASET_DIR)
    suggester.suggest()


if __name__ == "__main__":
    main()
