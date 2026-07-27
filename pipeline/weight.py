# Approximate densities in g/cm³
MATERIAL_DENSITY = {
    "plastic": 0.95,      # PET bottles, typical containers
    "glass": 2.5,
    "metal": 7.8,          # steel/generic metal average
    "wood": 0.6,
    "cardboard": 0.3,
    "ceramic": 2.3,
    "rubber": 1.1,
    "paper": 0.75,
}

def estimate_weight(volume_mm3, material, fill_ratio=1.0):
    """
    volume_mm3: from estimate_volume()
    material: string key from MATERIAL_DENSITY
    fill_ratio: accounts for hollow objects (e.g. an empty bottle
                isn't solid plastic all the way through) - 1.0 = solid,
                lower values = mostly hollow/shell-like
    """
    if material not in MATERIAL_DENSITY:
        raise ValueError(f"Unknown material: '{material}'. Choose from {list(MATERIAL_DENSITY.keys())}")

    density_g_per_mm3 = MATERIAL_DENSITY[material] / 1000  # g/cm³ → g/mm³
    weight_g = volume_mm3 * density_g_per_mm3 * fill_ratio

    return {
        "weight_g": round(weight_g, 1),
        "material": material,
        "fill_ratio_used": fill_ratio
    }