import pandas as pd
import create_list
import dl_file

doc_list = pd.read_csv("./data/doc_data.csv")
data = create_list.extract_fileid(doc_list)

data = dl_file.download_file(data)
data.to_csv("./data/update_doc_data.csv", index = False)