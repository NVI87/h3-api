import math
import random

import h3
from shapely.geometry import Polygon

from settings import settings


class HexIndexService:
    # методы не делал асинхронными, потому что все делается из памяти
    # блокировки (типа aiorwlock) не расставлял, потому что сценарии не предполагают одновременное чтение/запись
    def __init__(self, latitude: float, longitude: float, radius: float):
        self.hexes: list[list] = self.create_hexes(latitude, longitude, radius)

    def as_dict(self):
        return {_[0]: _ for _ in self.hexes}

    @staticmethod
    def create_hexes(
            latitude: float,
            longitude: float,
            radius: float,
    ) -> list[list]:
        """
        Создает массив данных вида [h3_index, level, cell_id]

        :param latitude: широта
        :param longitude: долгота
        :param radius: радиус области в км
        :return: массив списков с данными
        """
        center_cell = h3.latlng_to_cell(latitude, longitude, settings.base_resolution)

        # Плоское приближение
        full_square = math.pi * radius * radius

        # Инициализация шага кольца, площади гексагонов, множества гексагонов
        ring_radius, cells_square, cells = 0, 0, set()

        # Добавляем по дополнительному кольцу, пока совокупная площадь не достигнет площади целевой области
        while cells_square < full_square:
            ring_cells = h3.grid_ring(center_cell, ring_radius)
            cells_square += sum([h3.cell_area(cell) for cell in ring_cells])
            cells |= set(ring_cells)
            ring_radius += 1

        return [
            [
                cell,
                random.randint(settings.level_border_left, settings.level_border_right),
                random.randint(settings.cell_id_from,settings.cell_id_to)
            ] for cell in cells
        ]

    def hex(self, parent_hex: str) -> list:
        """
        Возвращает элементы массива исходного датасета входящих в заданный гексагон

        :param parent_hex: индекс гексагона
        :return: элементы массива исходного датасета входящих в заданный гексагон
        """
        h3_dict = self.as_dict()
        return [h3_dict[cell] for cell in h3.cell_to_children(parent_hex, settings.base_resolution) if cell in h3_dict]

    def bbox(self, polygon: Polygon) -> list:
        """
        Возвращает элементы массива исходного датасета входящих в заданные границы.

        :param polygon: полигон границ
        :return: элементы массива исходного датасета входящих в заданные границы
        """
        h3_dict = self.as_dict()
        return [h3_dict[cell] for cell in h3.geo_to_cells(polygon, settings.base_resolution) if cell in h3_dict]

    def avg(self, resolution: int):
        """
        Возвращает массив гексагонов заданного разрешения, с медианным значением level сгруппированным
        по cell_id из исходного датасета

        :param resolution: разрешение от 0 до 12
        :return: массив гексагонов заданного разрешения
        """
        result_dict = dict()

        for h3_index, level, cell_id in self.hexes:
            parent_h3_index = h3.cell_to_parent(h3_index, resolution)

            if (parent_h3_index, cell_id) not in result_dict:
                result_dict[(parent_h3_index, cell_id)] = [level]
            else:
                result_dict[(parent_h3_index, cell_id)].append(level)

        return [[*k, sorted(v)[len(v) // 2]] for k, v in result_dict.items()]


class HexIndexServiceCached(HexIndexService):
    """Если массив кэшировать, то методы .hex и .bbox работают быстрее"""
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._hexes_dict = super().as_dict()

    def as_dict(self):
        return self._hexes_dict
