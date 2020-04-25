from zss import simple_distance, Node, distance, Operation
import pdb

def print_tree(root):
    print Node.get_label(root)
    for c in Node.get_children(root):
        print_tree(c)


A = Node("f")
B = (
    Node("f")
        .addkid(Node("a")
            .addkid(Node("d"))
            .addkid(Node("c")
                .addkid(Node("b"))))
        .addkid(Node("e"))
    )

print "Original A"
print_tree(A)

print "Original B"
print_tree(B)


d_s, op = simple_distance(A,B, return_operations = True)
print d_s

def update_tree(root, old_child ,new_child):
    if root == None:
        return 
    if old_child in root.children:
        root.children.remove(old_child)
        root.addkid(new_child)
    for c in root.children:
        update_tree(c, old_child, new_child)


root = None

for i in op:
    # pdb.set_trace()
    # print i.__repr__()
    
    # print i
    # print "arg1", i.arg1
    # print "arg2", i.arg2

    if i.type == Operation.insert:
        print "Inserting"
        pdb.set_trace()

        if root!=None:
            root.addkid(i.arg2)
        else:
            root = i.arg2


    elif i.type == Operation.update:
        print "Updating"
        pdb.set_trace()

        update_tree(A, i.arg1, i.arg2)
        #traverse A and update node to B?

    elif i.type == Operation.match:
        pdb.set_trace()
        print "Matching"
        i.arg1.addkid(root)
        root = i.arg1

    elif i.type == Operation.remove:
        print "Removing"
        pdb.set_trace()


        pass




print "new A"
print_tree(A)

# print "new B"
# print_tree(B)
