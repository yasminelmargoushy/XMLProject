class TreeNode:
    def __init__(self, tag, attribute, level):
        self.Tag = tag
        self.Attribute = attribute
        self.Parent = None
        self.Child = []
        self.Text = ""
        self.level = level
        self.SelfClosed = False

    def GetTag(self):
        return self.Tag

    def SetParent(self, Parentnode):
        self.Parent = Parentnode

    def GetParent(self):
        return self.Parent

    def AddChild(self, Newnode):
        self.Child.append(Newnode)
        return Newnode

    def GetChildren(self):
        return self.Child

    def GetAttributes(self):
        return self.Attribute

    def SetText(self, text):
        self.Text = text

    def GetText(self):
        return self.Text

    def GetLevel(self):
        return self.level

    def SetSelfClosed(self):
        self.SelfClosed = True

    def GetSelfClosed(self):
        return self.SelfClosed


class Tree:
    def __init__(self, string):
        self.Rootnode = None
        self.CurrentParent = None
        self.IntialTags = []
        self.level = 0
        CurrentTag = ""
        CurrentText = ""
        CurrentTextChar = ""
        TagFlag = 0
        for i in range(len(string)):
            if TagFlag == 1 or string[i] == "<":
                CurrentTag = CurrentTag + string[i]
            else:
                CurrentText = CurrentText + string[i]
                if string[i] != " " and string[i] != "\n" and string[i] != "\t" and string[i] != "\r":
                    CurrentTextChar = CurrentTextChar + string[i]

            if string[i] == "<":
                if CurrentTextChar != "" and self.CurrentParent != None:
                    self.AddText(CurrentText)
                CurrentText = ""
                CurrentTextChar = ""
                TagFlag = 1
            elif string[i] == ">" and CurrentTag[1] != "/" and CurrentTag[1] != "!" and CurrentTag[1] != "?" and CurrentTag[-2] != "/":
                TagFlag = 0
                self.ParseTag(CurrentTag, False)
                CurrentTag = ""

            elif string[i] == ">" and CurrentTag[1] != "/" and CurrentTag[1] != "!" and CurrentTag[1] != "?" and CurrentTag[-2] == "/":
                TagFlag = 0
                CurrentTag = CurrentTag[:-2] + CurrentTag[-2 + 1:]
                self.ParseTag(CurrentTag, True)
                self.level -= 1
                self.CloseTag()
                CurrentTag = ""

            elif string[i] == ">" and (CurrentTag[1] == "!" or CurrentTag[1] == "?"):
                TagFlag = 0
                if CurrentTag[1] == "?":
                    self.IntialTags.append(CurrentTag)
                CurrentTag = ""

            elif string[i] == ">" and CurrentTag[1] == "/":
                TagFlag = 0
                self.level -= 1
                self.CloseTag()
                CurrentTag = ""

    def AddNode(self, tag , attribute, SelfClosed):
        Newnode = TreeNode(tag, attribute, self.level)
        Newnode.SetParent(self.CurrentParent)
        if SelfClosed == True:
            Newnode.SetSelfClosed()
        self.CurrentParent.AddChild(Newnode)
        self.CurrentParent = Newnode

    def AddText(self, text):
        self.CurrentParent.SetText(text)

    def CloseTag (self):
        if self.CurrentParent != None:
            self.CurrentParent = self.CurrentParent.GetParent()

    def ParseTag(self, FullTag, SelfClosed):
        attributes = {}
        CurrentString = ""
        Tag = ""
        CurrentAttribute = ""
        TFlag = 0
        AVFlag = 0
        if FullTag[1] == "?" or FullTag[1] == "!":
            return
        for i in FullTag:
            if i == "<":
                TFlag = 1
            elif (i == " " or i == ">") and TFlag == 1:
                TFlag = 0
                Tag = CurrentString
                CurrentString = ""
            elif i == '"' and AVFlag == 0:
                AVFlag = 1
            elif i == '"' and AVFlag == 1:
                AVFlag = 0
                CurrentValue = CurrentString
                CurrentString = ""
                attributes[CurrentAttribute] = CurrentValue
            elif i == "=" and TFlag == 0 and AVFlag == 0:
                if CurrentString[0:4] == "xml:":
                    CurrentString = CurrentString[4:]
                CurrentAttribute = CurrentString
                CurrentString = ""
            if (i != " " and i != "=" and i != "<" and i != ">" and i != '"') or (i == " " and AVFlag == 1) or (i == "=" and AVFlag == 1):
                CurrentString = CurrentString + i

        if self.Rootnode == None:
            Root = TreeNode(Tag, attributes, self.level)
            Root.SetParent(None)
            if SelfClosed == True:
                Root.SetSelfClosed()
            self.Rootnode = Root
            self.CurrentParent = Root
            self.level = 1
        else:
            self.AddNode(Tag, attributes, SelfClosed)
            self.level += 1

    def PrintJSONTree(self):
        CurrentNode = self.Rootnode
        String = "{\n  "
        String = String + f'"{self.Rootnode.GetTag()}": '
        String = String + self.PrintJSONNode(CurrentNode, False, 0)
        String = String + "\n}"
        return String
        #JSON_file = open('XML_TO_JSON.json', 'w')
        #JSON_file.write(String)
        #JSON_file.close()

    def PrintJSONNode(self, CurrentNode, RepeatedNode, extra):
        Attributes = CurrentNode.GetAttributes()
        Text = CurrentNode.GetText()
        Children = CurrentNode.GetChildren()
        Indentation = "  " * (CurrentNode.GetLevel() + 1 + extra)
        FirstFlag = 1
        if RepeatedNode == True:
            String = Indentation
        else:
            String = ""
        # Print Attriutes
        for i in Attributes:
            if FirstFlag == 1:
                String = String + "{\n" + Indentation + "  " + f'"@{i}": "{Attributes[i]}"'
                FirstFlag = 0
            else:
                String = String + ",\n" + Indentation + "  " + f'"@{i}": "{Attributes[i]}"'
        if Text == "" and len(Children) == 0 and len(Attributes) != 0:
            String = String + "\n" + Indentation + "}"
            return String

        # Print Text
        elif Text != "" and len(Attributes) == 0 and len(Children) == 0:
            String = String + f'"{Text}"'
            return String
        elif Text != "" and len(Attributes) == 0 and len(Children) != 0:
            String = String + "{\n" + Indentation + "  " + f'"#text": "{Text}"'
            FirstFlag = 0
        elif Text != "" and len(Attributes) != 0 and len(Children) == 0:
            String = String + ",\n" + Indentation + "  " + f'"#text": "{Text}"'
            String = String + "\n" + Indentation + "}"

        # Print Children
        if len(Children) != 0:
            MChildren = []
            ClusteredChild = []
            PreviousTag = Children[0].GetTag()
            ClusteredChild.append(Children[0])
            for i in range(1, len(Children)):
                if Children[i].GetTag() == PreviousTag:
                    ClusteredChild.append(Children[i])
                    PreviousTag = Children[i].GetTag()
                else:
                    MChildren.append(ClusteredChild)
                    ClusteredChild = []
                    ClusteredChild.append(Children[i])
                    PreviousTag = Children[i].GetTag()
            if len(ClusteredChild) != 0:
                MChildren.append(ClusteredChild)

            for ClChild in MChildren:
                if len(ClChild) == 1:
                    if FirstFlag == 1:
                        String = String + "{\n" + Indentation + "  " + f'"{ClChild[0].GetTag()}": '
                        String = String + self.PrintJSONNode(ClChild[0], False, extra)
                        FirstFlag = 0
                    else:
                        String = String + ",\n" + Indentation + "  " + f'"{ClChild[0].GetTag()}": '
                        String = String + self.PrintJSONNode(ClChild[0], False, extra)
                else:
                    if FirstFlag == 1:
                        String = String + "{\n" + Indentation + "  " + f'"{ClChild[0].GetTag()}": [\n'
                        FirstFlag = 0
                    else:
                        String = String + ",\n" + Indentation + "  " + f'"{ClChild[0].GetTag()}": [\n'
                    for k in range(len(ClChild)):
                        if k != 0:
                            String = String + ",\n"
                        String = String + self.PrintJSONNode(ClChild[k], True, extra + 1)
                    String = String + "\n" + Indentation + "  " + "]"
            String = String + "\n" + Indentation + "}"
        else:
            if Text == "" and len(Children) == 0 and len(Attributes) == 0:
                String = "[]"
        return String


def PrintJSONFile(StringFile):
    WorkingTree = Tree(StringFile)
    String = WorkingTree.PrintJSONTree()
    return String

def PrintMinifiedFile(StringFile):
    WorkingTree = Tree(StringFile)
    String = WorkingTree.PrintMinifiedTree()
    return String
