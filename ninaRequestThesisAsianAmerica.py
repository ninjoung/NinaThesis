
import json, sys, os, csv
#from print_progress import print_progress
#print('Opening file ' + sys.argv[1])

def dumpJsonAry(jsons, filename):
    with open(filename, "w", encoding='utf-8') as file:
         json.dump(jsons, file, indent=4, sort_keys=True, ensure_ascii=False)
    print("created new json file: {}".format(filename))

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    posts = json.load(f)
print('file opened')


assert (len(posts) != 0), 'posts cannot be empty'
if('metadata' in posts[0]):
    print("Post contains metadata tag. First element in list removed")
    posts.pop(0)

target_tags = {11304, 2788, 2912, 3506, 3508, 5580, 5581, 5602, 5808, 8340, 9053, 12368, 12370, 13026, 14377, 15344, 15862, 16313, 17399, 21776, 21777,
               22144, 5311, 5324,
               4335, 6545, 6930, 7406, 11294, 12046, 17980, 18485, 18802, 18872, 21525,
               4770, 5752, 7769, 19283, 21087, 21972, 22083,
               5691, 6797, 6867, 6869,
               11756,
               6196, 12813,
               18413,
               6475, 7507, 11082, 11646,
               2911, 4019, 6183, 11483, 15313, 15537, 15783,
               15514,
               7042, 8658, 10254, 13801,
               3292, 12814, 19822,
               12470}
target_strings = [
    "asian american center", "asian american studies","south asian studies", "Asian American Association", "Asian American studies minor", "asian", "asianamerican", "pan asian council", "east asian studies", "russian and asian languages and literatures", "south asian political action committee", "asian american", "asian americans", "tufts asian student coalition", "south asians", "south asian", "tufts association of south asians", "asian american community",
                  "korean students association","korean", "korean food",
#
                  "chinese progressive association", "chinese food", "chinese students", "chinese house", "chinese students association", "chinese culture", "chinese dance", "chinese mythology", "chinese music",
#
                  "japanese cuisine", "japanese art", "japanese food", "japanese film", "japanese house", "japanese music",
#
                  "vietnamese students", "vietnamese student", "vietnamese students club", "vietnamese americans", "vietnamese american",
#
                  "cambodian", "cambodian students", "cambodian student", "cambodian american", "cambodian americans",
#
                  "filipino", "filipino student", "filipino students"
#
                  "thai", "thai students association",
#
                  "tibetan", "tibetan student", "tibetan students",
#
                  "iranian american", "iranian americans", "iranian student", "iranian students",
#
                  "indian americans", "indian american", "indian student", "indian students", "indian", "indians",
#
                  "hawaiian", "hawaiian student", "hawaiian students",

                  "pacific islander", "pacific islanders", "pacific islands americans", "pacific islands american"
#
#                  "arab", "arabic", "arab student", "arab students", "tufts takht arabic ensemble",
#
#                  "ampt", "association of multiracial people at tufts", "multiracial", "multiracial student", "multiracial students",
#
#                  "culture clubs",

                  "start house", "aac", "asian american", "asian culture club", "asian culture clubs", "asian culture club"
                  #"korean", "japanese", "vietnamese", "filipino", "cambodian", "hmong", "lao", "hawaiian", "pacific islander", "pacific islands americans", "arabs"
]


data = []
for x in posts:
    isMatch = False
    if(x["analysis"]["sentiment_score"] == "Error"):
        continue

    tags_set = set(x["tags"])

    # I've created new keys for entries
    x["filtering"] = {}
    x["filtering"]["matched_tags"] = []
    x["filtering"]["matched_entities"] = [];

    if(tags_set & target_tags):
        x["filtering"]["matched_tags"] += list(tags_set.intersection(target_tags));
        isMatch = True

    # for filtering entities I have to use a set first since there may be duplicate
    # entities in each post (one with caps and the other without)
    entities_set = set()
    for entity in x["analysis"]["entitiy_sentiments"]:
        if(entity["name"].lower() in target_strings):
            entities_set.add(entity["name"].lower())
            isMatch = True
    x['filtering']['matched_entities'] = list(entities_set)

    if(isMatch == True):
        data.append(x)

dumpJsonAry(data, "dataRequest_Thesis_AsAmer{}.json".format(len(data)))
# dumpJsonAry(data, os.path.expanduser( "~/Desktop/enigmadailydata/requestResultsThesis/json/dataRequest_Thesis_AsAmer{}.json".format(len(data))))

with open('ThesisAsAmer{}.csv'.format(len(data)), 'w', encoding='utf-8', newline='') as csvfile:
# with open(os.path.expanduser('~/Desktop/enigmadailydata/requestResultsThesis/csv/ThesisAsAmer{}.csv'.format(len(data))), 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['post_id', 'date', 'title', 'author', 'sentiment_score', 'sentiment_magnitude', 'link', 'matched_tags', 'matched_entities']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    csvRow = {}
    for x in data:
        csvRow['post_id'] = x['id']
        csvRow['date'] = x['date']
        csvRow['title'] = x['title_text']
        csvRow['author'] = x['author']
        csvRow['sentiment_score'] = x['analysis']['sentiment_score']
        csvRow['sentiment_magnitude'] = x['analysis']['sentiment_magnitude']
        csvRow['link'] = x['link']

        # I decided to print out the list for tags directly due to how excel
        # treats them as numbers, and does some weird formatting on them
        csvRow['matched_tags'] = x['filtering']['matched_tags']
        csvRow['matched_entities'] = ','.join(x['filtering']['matched_entities'])
        writer.writerow(csvRow)

    print("created new csv file: {}".format(csvfile.name))
