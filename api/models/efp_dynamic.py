"""Every eFP database exposes the same sample_data table, so instead of hand-writing
~190 near-identical model files we generate one model class per database here."""

from api import db
from api.utils.bar_utils import load_combined_master

# Optional sample_data columns, keyed by the schema_variants role that declares them.
# A database only gets one of these if its assigned variant declares a column with that
# role, so every variant predating this mapping generates exactly the columns it did
# before. Each value is a factory: mapped_column objects cannot be shared between models.
_OPTIONAL_COLUMNS_BY_ROLE = {
    "value_std": lambda: db.mapped_column(db.Float, nullable=True),
}


def _optional_columns(variant):
    """Extra mapped columns this variant's sample_data declares, keyed by column name."""
    columns = variant.get("tables", {}).get("sample_data", {}).get("columns", {})
    return {
        column: _OPTIONAL_COLUMNS_BY_ROLE[spec["role"]]()
        for column, spec in columns.items()
        if spec.get("role") in _OPTIONAL_COLUMNS_BY_ROLE
    }


def _sample_data_model(database, variant):
    class_name = "".join(part.capitalize() for part in database.split("_")) + "SampleData"
    attributes = {
        "__bind_key__": database,
        "__tablename__": "sample_data",
        "data_probeset_id": db.mapped_column(db.String(255), primary_key=True),
        "data_bot_id": db.mapped_column(db.String(255), primary_key=True),
        "data_signal": db.mapped_column(db.Float, primary_key=True),
    }
    attributes.update(_optional_columns(variant))
    return type(class_name, (db.Model,), attributes)


_MASTER = load_combined_master()

# A few catalogued databases name a schema_variant that is not in schema_variants; they
# fall back to {} and so generate the three required columns only, exactly as before.
SAMPLE_DATA_MODELS = {
    database: _sample_data_model(database, _MASTER["schema_variants"].get(info["schema_variant"], {}))
    for database, info in _MASTER["databases"].items()
}
