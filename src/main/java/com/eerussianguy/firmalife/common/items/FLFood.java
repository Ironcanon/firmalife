package com.eerussianguy.firmalife.common.items;

import net.minecraft.world.food.FoodProperties;

public enum FLFood
{
    FROTHY_COCONUT,
    WHITE_CHOCOLATE_BLEND,
    DARK_CHOCOLATE_BLEND,
    MILK_CHOCOLATE_BLEND;

    private final boolean meat, fast;

    FLFood()
    {
        this(false, false);
    }

    FLFood(boolean meat, boolean fast)
    {
        this.meat = meat;
        this.fast = fast;
    }

    public FoodProperties getFoodProperties()
    {
        FoodProperties.Builder builder = new FoodProperties.Builder();
        if (meat) builder.meat();
        if (fast) builder.fast();
        return builder.nutrition(4).saturationMod(0.3f).build();
    }
}