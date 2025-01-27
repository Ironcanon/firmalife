package com.eerussianguy.firmalife.common.blockentities;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.items.ItemStackHandler;

import net.dries007.tfc.common.blockentities.InventoryBlockEntity;
import net.dries007.tfc.common.recipes.SimpleItemRecipe;
import net.dries007.tfc.common.recipes.inventory.ItemStackInventory;
import net.dries007.tfc.util.calendar.Calendars;
import org.jetbrains.annotations.Nullable;

public abstract class SimpleItemRecipeBlockEntity<T extends SimpleItemRecipe> extends InventoryBlockEntity<ItemStackHandler>
{
    private final int duration;
    protected long startTick;
    @Nullable protected T cachedRecipe;

    public SimpleItemRecipeBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state, Component defaultName, int duration)
    {
        super(type, pos, state, defaultInventory(1), defaultName);
        this.duration = duration;
    }

    @Override
    public void loadAdditional(CompoundTag nbt)
    {
        startTick = nbt.getLong("startTick");
        super.loadAdditional(nbt);
        updateCache();
    }

    @Override
    public void saveAdditional(CompoundTag nbt)
    {
        nbt.putLong("startTick", startTick);
        super.saveAdditional(nbt);
    }

    @Override
    public int getSlotStackLimit(int slot)
    {
        return 1;
    }

    abstract void updateCache();

    public void start()
    {
        assert level != null;
        updateCache();
        if (cachedRecipe != null)
        {
            startTick = Calendars.SERVER.getTicks();
            if (!level.canSeeSky(worldPosition.above()))
            {
                startTick += duration; // takes twice as long indoors
            }
            markForSync();
        }
    }

    public void finish()
    {
        final T recipe = this.cachedRecipe;
        if (recipe != null)
        {
            final ItemStack out = recipe.assemble(new ItemStackInventory(readStack()));
            inventory.setStackInSlot(0, out);
            updateCache();
            markForSync();
        }
    }

    public ItemStack insert(ItemStack item)
    {
        return inventory.insertItem(0, item, false);
    }

    public ItemStack extract()
    {
        return inventory.extractItem(0, 1, false);
    }

    public ItemStack readStack()
    {
        return inventory.getStackInSlot(0).copy();
    }

    public int getDuration()
    {
        return duration;
    }
}
