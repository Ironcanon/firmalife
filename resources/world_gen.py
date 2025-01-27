from typing import Union, get_args

from mcresources import ResourceManager, utils
from mcresources.type_definitions import ResourceIdentifier, JsonObject, Json, VerticalAnchor

from constants import *

def generate(rm: ResourceManager):
    placed_feature_tag(rm, 'in_biome/veins', *['firmalife:vein/%s' % v for v in ORE_VEINS.keys()])

    for vein_name, vein in ORE_VEINS.items():
        rocks = expand_rocks(vein.rocks, vein_name)
        configured_placed_feature(rm, ('vein', vein_name), 'tfc:%s_vein' % vein.type, {
            'rarity': vein.rarity,
            'min_y': utils.vertical_anchor(vein.min_y, 'absolute'),
            'max_y': utils.vertical_anchor(vein.max_y, 'absolute'),
            'size': vein.size,
            'density': vein_density(vein.density),
            'blocks': [{
                'replace': ['tfc:rock/raw/%s' % rock],
                'with': vein_ore_blocks(vein, rock)
            } for rock in rocks],
            'indicator': {
                'rarity': 12,
                'blocks': [{
                    'block': 'firmalife:ore/small_%s' % vein.ore
                }]
            },
            'random_name': vein_name,
            'biomes': vein.biomes
        })

def placed_feature_tag(rm: ResourceManager, name_parts: ResourceIdentifier, *values: ResourceIdentifier):
    return rm.tag(name_parts, 'worldgen/placed_feature', *values)

def configured_feature_tag(rm: ResourceManager, name_parts: ResourceIdentifier, *values: ResourceIdentifier):
    return rm.tag(name_parts, 'worldgen/configured_feature', *values)

def biome_tag(rm: ResourceManager, name_parts: ResourceIdentifier, *values: ResourceIdentifier):
    return rm.tag(name_parts, 'worldgen/biome', *values)

def vein_ore_blocks(vein: Vein, rock: str) -> List[Dict[str, Any]]:
    ore_blocks = [{
        'weight': vein.poor,
        'block': 'firmalife:ore/poor_%s/%s' % (vein.ore, rock)
    }, {
        'weight': vein.normal,
        'block': 'firmalife:ore/normal_%s/%s' % (vein.ore, rock)
    }, {
        'weight': vein.rich,
        'block': 'firmalife:ore/rich_%s/%s' % (vein.ore, rock)
    }]
    if vein.spoiler_ore is not None and rock in vein.spoiler_rocks:
        p = vein.spoiler_rarity * 0.01  # as a percentage of the overall vein
        ore_blocks.append({
            'weight': int(100 * p / (1 - p)),
            'block': 'firmalife:ore/%s/%s' % (vein.spoiler_ore, rock)
        })
    elif vein.deposits:
        ore_blocks.append({
            'weight': 10,
            'block': 'firmalife:deposit/%s/%s' % (vein.ore, rock)
        })
    return ore_blocks

def expand_rocks(rocks_list: List[str], path: Optional[str] = None) -> List[str]:
    rocks = []
    for rock_spec in rocks_list:
        if rock_spec in TFC_ROCKS:
            rocks.append(rock_spec)
        elif rock_spec in ROCK_CATEGORIES:
            rocks += [r for r, d in TFC_ROCKS.items() if d.category == rock_spec]
        else:
            raise RuntimeError('Unknown rock or rock category specification: %s at %s' % (rock_spec, path if path is not None else '??'))
    return rocks

def vein_density(density: int) -> float:
    assert 0 <= density <= 100, 'Invalid density: %s' % str(density)
    return round(density * 0.01, 2)

def configured_placed_feature(rm: ResourceManager, name_parts: ResourceIdentifier, feature: Optional[ResourceIdentifier] = None, config: JsonObject = None, *placements: Json):
    res = utils.resource_location(rm.domain, name_parts)
    if feature is None:
        feature = res
    rm.configured_feature(res, feature, config)
    rm.placed_feature(res, res, *placements)

