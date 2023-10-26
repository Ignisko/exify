# The function is expected to return an INTEGER_DOUBLY_LINKED_LIST.
# The function accepts INTEGER_DOUBLY_LINKED_LIST llist as parameter.
#

#
# For your reference:
#
# DoublyLinkedListNode:
#     int data
#     DoublyLinkedListNode next
#     DoublyLinkedListNode prev
#
def reverse(llist):
    current = llist
    prev = None

    while current:
        next_node = current.next
        current.next = prev
        current.prev = next_node
        prev = current
        current = next_node

    return prev