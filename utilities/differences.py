# Import dependencies
import pandas as pd


# Define function that will identify the changes between the old and new reports
def diff_dataframe(old_df, new_df, key_cols):
    """
    Compare two DataFrames (old vs new) based on a set of key columns.
    Return a DataFrame that includes *all* rows/columns from both.
    
    - For NEW rows (in new_df only), show the new data.
    - For DELETED rows (in old_df only), show the old data.
    - For rows in both:
        * If a cell is unchanged, show the new value.
        * If changed, show "old → new".
    
    A "RowStatus" column indicates 'NEW', 'DELETED', 'CHANGED', or 'UNCHANGED'.

    The returned tables retain the column order from old_df, appending any
    truly new columns from new_df at the end.
    """
    
    # Create copies to prevent altering the originals
    old_df = old_df.copy()
    new_df = new_df.copy()
    
    # Convert key columns to string to avoid dtype conflicts
    for col in key_cols:
        old_df[col] = old_df[col].astype(str)
        new_df[col] = new_df[col].astype(str)

    # Set index
    old_df.set_index(key_cols, inplace=True)
    new_df.set_index(key_cols, inplace=True)
    
    # Build final columns in the order of old, then append missing from new
    all_cols_order = list(old_df.columns)
    for c in new_df.columns:
        if c not in all_cols_order:
            all_cols_order.append(c)

    # Reindex both DataFrames to have the same columns in the final order
    old_df = old_df.reindex(columns=all_cols_order)
    new_df = new_df.reindex(columns=all_cols_order)
    
    # Union of all row indices
    full_index = old_df.index.union(new_df.index)
    old_df = old_df.reindex(full_index)
    new_df = new_df.reindex(full_index)
    
    # Create the diff DataFrame using the final column order
    diff_df = pd.DataFrame(index=full_index, columns=all_cols_order, dtype="object")
    
    # Identify new-only rows, deleted-only rows, and rows in both
    new_only_mask = old_df.isna().all(axis=1) & new_df.notna().any(axis=1)
    deleted_mask = new_df.isna().all(axis=1) & old_df.notna().any(axis=1)
    both_mask = ~(new_only_mask | deleted_mask)
    
    # Fill new-only rows with the new data
    diff_df.loc[new_only_mask, :] = (
        new_df.loc[new_only_mask].fillna('').astype(str).values
    )
    
    # Fill deleted-only rows with the old data
    diff_df.loc[deleted_mask, :] = (
        old_df.loc[deleted_mask].fillna('').astype(str).values
    )
    
    # For rows in both, compare cell by cell
    old_sub = old_df.loc[both_mask].fillna("")
    new_sub = new_df.loc[both_mask].fillna("")
    
    for col in all_cols_order:
        # If unchanged, place the new value
        diff_df.loc[both_mask, col] = new_sub.loc[both_mask, col].values
        
        # If it was changed changed, show "old → new"
        changed_mask = old_sub[col] != new_sub[col]
        changed_index = changed_mask[changed_mask].index
        diff_df.loc[changed_index, col] = (
            old_sub.loc[changed_index, col].astype(str)
            + " → "
            + new_sub.loc[changed_index, col].astype(str)
        ).values
        
    # Add a column "RowStatus" to identify the rows that have are new/deleted/both
    # BOTH values will be overwritten to identify if there have been any values that were changed 
    row_status = pd.Series(index=full_index, dtype="object")
    row_status.loc[new_only_mask] = "NEW"
    row_status.loc[deleted_mask] = "DELETED"
    row_status.loc[both_mask]    = "BOTH"
    
    # Insert RowStatus as the first column, will be after the index keys
    diff_df.insert(0, "RowStatus", row_status)
    
    # Alter the RowStatus column to identify changed or unchanged rows that are in both reports
    for index, row in diff_df.iterrows():
        if row['RowStatus'] == 'BOTH':
            row_str = "".join(str(x) for x in diff_df.loc[index, all_cols_order])
            if " → " in row_str:
                diff_df.at[index, 'RowStatus'] = 'CHANGED'
            else:
                diff_df.at[index, 'RowStatus'] = 'UNCHANGED'
    
    # Move index key columns back 
    diff_df.reset_index(inplace=True)
    
    return diff_df
