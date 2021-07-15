from JSONConversion_Minifying import Tree


def Parsing(XML):
    tag = ""
    tags = []
    tag_start = False
    ill = False
    for ch, i in zip(XML, range(len(XML))):
        if (ch == '!' and tag_start) or (ch == '?' and tag_start):
            tag_start = False
            continue
        if ch == '/':
            continue
        if ch == '<':
            tag_start = True
            continue
        if ch == ' ' and tag_start:
            tag_start = False
        if ch == '>' and tag != '':
            if XML[i - 1] != '/':
                tags.append(tag)
            tag = ""
            tag_start = False
        if tag_start:
            tag += ch
    return tags


def is_consistent(tags):
    is_con = True
    con = []
    for t in tags:
        if len(con) == 0:
            con.append(t)
            continue
        if t == con[len(con) - 1]:
            con.pop()
        else:
            con.append(t)

    if len(con) != 0:
        is_con = False
    return is_con


def ErrorDetection(XML):
    if outOfBounceDetect(XML) + openAndClosedTagsDetect(XML) == "":
        return "NO Error"
    else:
        return outOfBounceDetect(XML) + openAndClosedTagsDetect(XML)


def outOfBounceDetect(XML):
    error = ""
    tag, i1, is_closed_tag1, l1 = getNextTag(XML)
    first_tag = tag
    next_tag, i2, is_closed_tag2, l2 = getNextTag(XML[i1:], l1)
    i2 = i2 + i1
    while True:
        if tag != next_tag or (is_closed_tag1 and not is_closed_tag2):
            for ch in XML[i1:i2]:
                if ch == ' ' or ch == '\n':
                    continue
                elif ch == '<':
                    tag = next_tag
                    is_closed_tag1 = is_closed_tag2
                    i1 = i2
                    l1 = l2
                    next_tag, i2, is_closed_tag2, l2 = getNextTag(XML[i1:], l1)
                    i2 = i2 + i1
                    break
                else:
                    error += "out of bounce in line " + str(l1) + '\n'
                    tag = next_tag
                    is_closed_tag1 = is_closed_tag2
                    i1 = i2
                    l1 = l2
                    next_tag, i2, is_closed_tag2, l2 = getNextTag(XML[i1:], l1)
                    i2 = i1 + i2
                    break
        elif tag == next_tag and not is_closed_tag1 and is_closed_tag2:
            tag = next_tag
            is_closed_tag1 = is_closed_tag2
            i1 = i2
            l1 = l2
            next_tag, i2, is_closed_tag2, l2 = getNextTag(XML[i1:], l1)
            i2 = i2 + i1
        if first_tag == next_tag:
            break
    return error  # outO   #out


def openAndClosedTagsDetect(XML):
    error = ""
    tag, i1, is_closed_tag1, l1 = getNextTag(XML)
    first_tag = tag
    next_tag, i2, is_closed_tag2, l2 = getNextTag(XML[i1:], l1)
    i2 = i2 + i1
    l2 = 0
    is_tag = False
    is_data = False
    is_parent = False
    tag_is_open = False
    error_raise = False
    XML_end = False
    update = False
    nano = False
    tags_waiting_close = []
    while True:
        XML_end = False
        if is_closed_tag1:
            if not nano and tags_waiting_close[len(tags_waiting_close) - 1] == tag:
                update = True
                tags_waiting_close.pop()
                if len(tags_waiting_close) == 0:
                    return error
                continue
        if nano:
            if len(tags_waiting_close) == 0:
                return error
        i = i1
        temp_tag, temp_i, temp_is_closed_tag, temp_l = getNextTag(XML[i:], l1)
        temp_i = temp_i + i
        if update:
            tag = temp_tag
            is_closed_tag1 = temp_is_closed_tag
            i1 = temp_i
            l1 = temp_l
            error_raise = False
            i = i1
            if tag != first_tag:
                temp_tag, temp_i, temp_is_closed_tag, temp_l = getNextTag(XML[i:], l1)
                temp_i = temp_i + i
            else:
                nano = True
            update = False
        if tag == next_tag and is_closed_tag1 == is_closed_tag2 and tag != first_tag:
            in_while = True
        while tag != next_tag and i <= len(XML) or in_while:
            if not nano:
                next_tag, i2, is_closed_tag2, l2 = getNextTag(XML[i:], l1)
                i = i2 + i
            else:
                next_tag = tag
            in_while = False
            if next_tag == first_tag:
                XML_end = True
                break
        if tag == next_tag and not is_closed_tag1 and is_closed_tag2:
            is_tag = False
            is_data = False
            for ch in XML[i1:]:
                if ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r':
                    continue
                elif ch == '<':  # open tag exist in next
                    is_tag = True
                    break
                else:
                    is_data = True
            if is_data and is_tag:
                next, i3, is_closed_tag3, l3 = getNextTag(XML[i1:], l1)
                if tag != next:  # error
                    error += "Tag " + tag + " in line " + str(l1) + " Missing it`s closed tag" + '\n'
                    error_raise = True
            elif is_tag:
                is_parent = True
        elif tag == next_tag and not is_closed_tag1 and not is_closed_tag2:
            error += "Tag " + tag + " in line " + str(l1) + " Missing it`s closed tag" + '\n'
            error_raise = True
        elif tag == next_tag and is_closed_tag1 and not is_closed_tag2 and tags_waiting_close[
            len(tags_waiting_close) - 1] != tag:
            error += "Tag " + tag + " in line " + str(l1) + " Missing it`s open tag" + '\n'
            error_raise = True
        elif tag != next_tag and not is_closed_tag1 and XML_end:
            error += "Tag " + tag + " in line " + str(l1) + " Missing it`s closed tag" + '\n'
            error_raise = True
            XML_end = False
        if not is_closed_tag1 and not error_raise:
            tags_waiting_close.append(tag)
        elif is_closed_tag1:
            if tags_waiting_close[len(tags_waiting_close) - 1] == tag:
                tags_waiting_close.pop()
        tag = temp_tag
        is_closed_tag1 = temp_is_closed_tag
        i1 = temp_i
        l1 = temp_l
        error_raise = False


def ErrorCorrection(XML):
    er = openAndClosedTagsDetect(XML)
    op_er = False
    if "Missing it`s open tag" in er:
        op_er = True
    if not op_er:
        return Formatting(XML)
    else:
        return "sorry can`t be corrected"


def getNextTag(XML, old_no_line=1):
    no_line = old_no_line
    tag = ""
    next_tag = ""
    is_closed_tag = False
    tag_start = False
    ill = False
    for ch, i in zip(XML, range(len(XML))):
        if ch == '\n':
            no_line += 1
        if (ch == '!' and tag_start) or (ch == '?' and tag_start):
            tag_start = False
            continue
        if ch == '/' and tag_start:
            is_closed_tag = True
            continue
        if ch == '<':
            tag_start = True
            continue
        if ch == ' ' and tag_start:
            tag_start = False
        if ch == '>' and tag != '':
            if XML[i - 1] != '/':
                return tag, i + 1, is_closed_tag, no_line
            else:
                tag = ""
        if tag_start:
            tag += ch


# interfacing
def Formatting(XML):
    XMLTree = Tree(XML)
    XMLReturn = ""
    first_tag, index, f, f = getNextTag(XML)
    for i, ch in zip(range(len(XML[:index])), XML):
        XMLReturn += ch
    m = XMLReturn.split("\n")
    XMLReturn = "\n".join(m[:-1])
    return XMLReturn + '\n' + recFormatting(XMLTree.Rootnode)


def recFormatting(subParent, XML=""):
    taps = ""
    for t in range(subParent.GetLevel()):
        taps += '\t'
    if subParent.SelfClosed:
        at = ""
        if len(subParent.GetAttributes().keys()) != 0:
            for tag, item in subParent.GetAttributes().items():
                at += tag + '="' + item + '"' + ' '
            XML += taps + '<' + subParent.GetTag() + ' ' + at[:-1] + '/>'
        else:
            XML += taps + '<' + subParent.GetTag() + '/>'
    else:
        at = ""
        if len(subParent.GetAttributes().keys()) != 0:
            for tag, item in subParent.GetAttributes().items():
                at += tag + '="' + item + '"' + ' '
            XML += taps + '<' + subParent.GetTag() + ' ' + at[:-1] + '>'
        else:
            XML += taps + '<' + subParent.GetTag() + '>'
    if len(subParent.GetChildren()) != 0:
        XML += '\n'
        for child in subParent.GetChildren():
            XML = recFormatting(child, XML)
        XML += taps + "</" + subParent.GetTag() + '>' + '\n'
        return XML
    else:
        if not subParent.SelfClosed:
            XML += subParent.GetText() + "</" + subParent.GetTag() + '>' + '\n'
        else:
            XML += '\n'
        return XML



