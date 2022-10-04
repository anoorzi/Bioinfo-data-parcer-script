import argparse
import pandas as pd
import os
import numpy as np


## python3 data_parcer.py --data_path MK-6482_2022-07-25_16-45-01_V4.0_updated_reviewed.xls

def check_manifest(data_path):

    if not os.path.exists(data_path):
        raise Exception("File does not exist")
    else:
        
        ## Create Data frame with filter for only columns containing "Allele" Gene and "CYP2C19" Type for PF_Domain Sheet
        
        pf_worksheet = pd.read_excel(data_path, sheet_name='PF_Domain')
        pf_rslt_df = pf_worksheet[pf_worksheet['PFTEST'] == 'Allele'] 
        pf_final_df = pf_rslt_df[pf_rslt_df['PFGENRI'] == 'CYP2C19'] 

        ## Create Data frame with filter for only columns containing "CYP2C19" Type for PF_Domain Sheet

        sb_worksheet = pd.read_excel(data_path, sheet_name='SB_Domain')
        sb_rslt_df = sb_worksheet[sb_worksheet['SBGENRI'] == 'CYP2C19'] 
        
        ## Filter PF Data Frame to only have desired Columns "USUBJID", "PFORRES", "PFSEQ" and merge column "SBSEQ" for better data understanding
        pf_final = pf_final_df[["USUBJID", "PFORRES", "PFSEQ"]].sort_index(ignore_index=True)
        
        merge_data = sb_rslt_df[["USUBJID","SBSEQ"]].sort_index(ignore_index=True)
        
        pf_final = pd.merge(pf_final, merge_data, on="USUBJID", how="left")
        
        ## Remove the 'CYP2C19 ' prefix from the "SBMRKRID" so data can be compared 

        sb_final = sb_rslt_df[["USUBJID", "SBMRKRID"]].sort_index(ignore_index=True).apply(lambda S:S.str.replace('CYP2C19 ',""))

        ## Compare all the 'PFORRES' for PF_Domain and 'SBMRKRID' for SB_Domin and output a true or false column onto the data frame if the values match or not

        pf_final['match'] = np.where(pf_final['PFORRES'] == sb_final['SBMRKRID'], 'True', 'False')
        
        ## Extract All False from the dataframe (Non-matching values)
        
        pf_final = pf_final[pf_final['match'] == 'False'].sort_index(ignore_index=True)
        
        ## Merge the from SB_Domain "SBMRKRID" onto the final dataframe
        
        pf_final = pd.merge(pf_final, sb_final, on="USUBJID", how="left")
        
        print(pf_final)


if __name__=='__main__':
    # Step 1. Establishing Database Connection
    PARSER = argparse.ArgumentParser(
            description="Bio Informatics Parcer",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    PARSER.add_argument(
            "--data_path",
            type=str,
            help="Path to Manifest File",
        )

    args = PARSER.parse_args()
    check_manifest(args.data_path)