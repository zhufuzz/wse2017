# -*- coding:utf-8 -*-   x
#栈的实现

class Stack():
    def __init__(st,size):
        st.stack=[];
        st.size=size;
        st.top=-1;

    def push(st,content):
        if st.Full():
            print "Stack is Full!"
        else:
            st.stack.append(content)
            st.top=st.top+1

    def out(st):
        if st.Empty():
            print "Stack is Empty!"
        else:
            st.top=st.top-1
    def Full(st):
        if  st.top==st.size:
            return True
        else:
            return False
    def Empty(st):
        if st.top==-1:
            return True
        else:
            return False
