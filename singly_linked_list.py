#singly _linked_list#
class Node:
	def __init__(self,data):
		self.data=data
		self.next=Node

class Linked_list:
	def __init__(self):
		self.head=None

	def insert_tail(self,data):
		if self.head is None:
			self.insert_head(data)
		else:
			temp=self.head
			while temp.next!=None:
				temp=temp.next
			temp.next=Node(data)

	def insert_head(self,data):
		newNod=Node(data)
		if self.head!=None:
			newNod.next=self.head
		self.head=newNod

	def printList(self):
		temp=self.head
		while temp is not None:
			print(temp.data)
			temp=temp.next

	def delete_head(self):  #返回的是头结点
		temp=self.head
		if self.head!=None:
			self.head=self.head.next
			temp.next=None
		return temp

	def delete_tail(self):  #返回的是尾结点
		temp=self.head
		if self.head!=None:
			if self.head.next is None:
				self.head=None
			else:
				while temp.next.next is not None:
					temp=temp.next
				temp.next,temp=(None,temp.next)
		return temp

def isEmpty(self):
	return self.head is None

def reverse(self):  #逆置链表
	prev=None
	current=self.head
	while current:
		next_node=current.next
		current.next=prev
		prev=current
		current=next_node
	self.head=prev

def main():
	A=Linked_list()
	print("inserting 1st at head")
	a1=input()
	A.insert_head(a1)
	print("inserting 2nd at head")
	a2=input()
	A.insert_head(a2)
	print("\n print list：")
	A.printList()
	print("\ninserting 1st at tail")
	a3=input()
	A.insert_tail(a3)
	print("inserting 2nd at tail")
	a4=input()
	A.insert_tail(a4)
	print("\n print list:")
	A.printList()
	print("\ndelete list")
	A.delete_head()
	print("delete tail")
	A.delete_tail()
	print("\n print list")
	A.printList()
	print("\nreverse linked list")
	A.reverse()
	print("\nprint list")
	A.printList()

if __name__=="__main__":
	main()