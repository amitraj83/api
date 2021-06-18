


def carAndRankMap(rank_data):
    data = {}
    if rank_data['model_id']['0'] != None:
        data[int(rank_data['model_id']['0'])] = int(rank_data['rnk_consolidate_final']['0'])
    if rank_data['model_id']['1'] != None:
        data[int(rank_data['model_id']['1'])] = int(rank_data['rnk_consolidate_final']['1'])
    if rank_data['model_id']['2'] != None:
        data[int(rank_data['model_id']['2'])] = int(rank_data['rnk_consolidate_final']['2'])
    return data
#list(rank_data)[5] name
#rank_data[list(rank_data)[5]][list(rank_data[list(rank_data)[5]])[1]] value

def getCategorizedSpecs(rank_data):
    details = []
    for i in range(len(list(rank_data))):
        name = list(rank_data)[i]
        detail = {"name":name}
        for j in range(len(list(rank_data[list(rank_data)[i]]))):
            value = rank_data[list(rank_data)[i]][list(rank_data[list(rank_data)[i]])[j]]
            detail["car"+str(int(j+1))] = value
        details.append(detail)
    print("")
    return details

def getDescriptions(blog_content):
    descriptions = []
    headings = blog_content["jsonTemplate"]["line3H3Heading"]
    for i in range(len(headings)):
        title = headings[i]
        content = blog_content["jsonTemplate"]["line3"][i]
        descriptions.append({"title":title, "content":content})
    return descriptions

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")