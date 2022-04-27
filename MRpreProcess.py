from mrjob.job import MRJob
import re
import langdetect
class MRpreProcess(MRJob):
    # Booleans to ignore everything inside multi-line script and style tags
    inscript = False 
    instyle = False

    # Booleans to keep track of the uri of the current site and whether we're in the meta data or html code
    indoctype = False
    current_uri = None
    current_dict = None 

    def mapper(self, _, line):
        ##YIELD FLAGS:
        dictionaryTag = "DICT"
        dateTag = "DATE"
        lineTag = "LINE"
        strippedLineTag = "STRIPPED"

            # Add site uri and domain-name ##XX: creating the dictionary for the first time //mapper as temp var but no yield with var
        if "WARC-Target-URI:" in line:
            # Extract uri (unique key)
            uri_start = line.find("http")
            self.current_uri = line[uri_start:].replace("\n", "")
            # Extract domain name (feature)
            domain_start = uri_start + 7
            domain_end = line.find("/", domain_start)
            domain = line[domain_start:domain_end]
            # Make an entry for a new site
            self.current_dict = { "target-domain": domain, "content-raw": [], "content-stripped": [] }

        if line == "WARC/1.0\n": ## use this in mapper to yield dict  as dict flag
            # Mark the end of a previous site's source code
            self.indoctype = False
            self.inscript = False
            self.instyle = False
            if self.current_uri != None:
                temp = self.current_uri #XXXXXXXXXXXXXXXXXXX
                self.current_uri = None
                final_dict = (self.current_dict, dictionaryTag)
                yield temp, final_dict

                # Add date (This is hardcoded to common crawl's warc format) ##XX: adding date parameter to dictrionary as date flag in mapper
        if not self.indoctype:
            if line.find("Date:") == 0:
                try:
                    day = line[11:13] # %d
                    month = line[14:17] # %b
                    year = line[18:22] # %Y
                    datestring = f"{day}/{month}/{year}"
                    yieldDate = (datestring, dateTag) ##could be other variable clas with date?
                    yield self.current_uri, yieldDate
                except:
                    # Probably happens if trying to fetch date from a different curling software
                    print("Formatting error")  

        # Mark the start of the site's source code ##XX in mapper
        if line.find("<!DOCTYPE") == 0:
            self.indoctype = True

        # Add raw and stripped source code  ##XX: adding actual text data to dictionary in mapper as content flag
        if self.indoctype:
            # Append raw source code

            """
            Strip lines of source code and add the stripped data:
            """
            # Toggle boolean if inside script tag (multi-line)
            if line.find("<script") != -1:
                self.inscript = True
            if line.find("</script") != -1 and line.find("<script") == -1:
                self.inscript = False
                yield_line = (line, lineTag)
                yield self.current_uri, yield_line

            # Toggle boolean if inside style tag (multi-line)
            if line.find("<style") != -1:
                self.instyle = True
            if line.find("</style") != -1 and line.find("<style") == -1:
                self.instyle = False
                yield_line = (line, lineTag)
                yield self.current_uri, yield_line

            # Remove html tags
            if not self.inscript and not self.instyle:
                while line.find("<") != -1:
                    tagstart = line.find("<")
                    tagend = line.find(">", tagstart)
                    # Look for the end of the html tag, otherwise remove entire line due to the tag being multi-lined
                    if tagend == -1:
                        line = line[0:tagstart]
                    else:
                        line = line[0:tagstart] + line[tagend+1::]

                # regex to remove multi-line inline css attributes, e.g: someatrib1="somevalue1", someatrib2="somevalue2" >
                line = re.sub(r'[a-z_0-9]+ *= *"[a-zA-z0-9 -:;]*" *>*', "", line)
                line = re.sub(r'-*>*', "", line)
                #line = line.strip(" ").replace("\n", "")
                yield_line = (line, strippedLineTag)
                yield self.current_uri, yield_line

        

    def combiner_old(self, key, values):
        #current_dict = { "target-domain": None, "date": None, "content-raw": [], "content-stripped": [] }
        current_dict = []
        for x in values:
            try:
                test = len(x)
                current_dict.append(x[5])
            except:
                continue               
        yield key, current_dict 


      
    def reducer(self, key, values):

        current_dict = { "target-domain": None, "date": None, "content-raw": [], "content-stripped": [] }
        #processed_dict = {}

        for x in values:
            if x[1] == "STRIPPED":
                current_dict["content-stripped"].append(x[0])
                
            if x[1] == "LINE":
                current_dict["content-raw"].append(x[0]) 
                
            if x[1] == "DOMAIN":
                current_dict["target-domain"]= x[0] 
                
            if x[1] == "DATE":
                current_dict["date"]= x[0] 
                
        # Combine all stripped lines from previous site
        stripped_oneline = "".join(current_dict["content-stripped"]).lower()
        # Remove all symbols and punctuations, only allow extended latin and cyrillic characters in groups of 2 or more
        current_dict["content-tokens"] = re.findall(r'[0-9a-zà-öø-ÿа-яА-Я]{2,}', stripped_oneline)
        current_dict["content-oneline"] = " ".join(current_dict["content-tokens"])
        # Detect language of site
        try:
            lang = langdetect.detect(current_dict["content-oneline"])
            current_dict["language"] = lang
        except:
            pass
            # Most likely happens if no text could be successfully extracted from the site
            #print(f"Language could not be detected for site: {key}")
        # Reset current uri while we're looking for the uri of the next site
   
        yield key, current_dict  


if __name__ == '__main__':
    MRpreProcessc.run()