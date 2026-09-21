from api import db


class UmapCoords(db.Model):
    __bind_key__ = "arabidopsis_NIE_umap"
    __tablename__ = "umap_coords"

    cell_id: db.Mapped[int] = db.mapped_column(db.Integer, nullable=False, primary_key=True)
    umap_1: db.Mapped[float] = db.mapped_column(db.Float, nullable=False)
    umap_2: db.Mapped[float] = db.mapped_column(db.Float, nullable=False)
    cell_type: db.Mapped[str] = db.mapped_column(db.String(128), nullable=False)


class UmapExpression(db.Model):
    __bind_key__ = "arabidopsis_NIE_umap"
    __tablename__ = "umap_expression"

    gene_id: db.Mapped[str] = db.mapped_column(db.String(32), nullable=False, primary_key=True)
    expression: db.Mapped[dict] = db.mapped_column(db.JSON, nullable=False)
