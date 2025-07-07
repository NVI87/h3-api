from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    base_resolution: int = Field(
        12,
        description="",
        alias="BASE_H3_RESOLUTION"
    )

    center_point_lat: float = Field(
        56.0,
        description="",
        alias="CENTER_POINT_LATITUDE"
    )

    center_point_lon: float = Field(
        38.0,
        description="",
        alias="CENTER_POINT_LONGITUDE"
    )

    base_area_radius: float = Field(
        7.0,
        description="",
        alias="BASE_AREA_RADIUS"
    )

    level_border_left: int = Field(
        -120,
        description="",
        alias="LEVEL_BORDER_LEFT"
    )

    level_border_right: int = Field(
        -47,
        description="",
        alias="LEVEL_BORDER_RIGHT"
    )

    cell_id_from: int = Field(
        0,
        description="",
        alias="CELL_ID_FROM"
    )

    cell_id_to: int = Field(
        100,
        description="",
        alias="CELL_ID_TO"
    )


settings = Settings()
