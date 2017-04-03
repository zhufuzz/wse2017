#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "codegen.h"
#include "symboltable.h"
#include "stringbuffer.h"

extern void yyerror(char* msg);

static stringBuffer* staticVariableBuffer;
static stringBuffer* classInitBuffer;
static stringBuffer* currentMethodBuffer;
static stringBuffer* finishedMethodsBuffer;
static stringBuffer* mainBuffer;

static int currentMethodBufferIndex;
static int currentMethodStackSize;
static int currentMethodStackSizeMax;
static int currentMethodNumberOfLocals;

static int classInitBufferIndex;
static int classInitStackSize;
static int classInitStackSizeMax;

static int labelCounter = 0;
static int global       = 1;

char tempString[MAX_LENGTH_OF_COMMAND];

extern char* className;        /* from minako-syntax.y */

/* forward declarations */
static void increaseStackby(int stackdiff);
char convertType(int type);

void codegenInit() {
	staticVariableBuffer  = newStringBuffer();
	classInitBuffer       = newStringBuffer();
	currentMethodBuffer   = 0;
	finishedMethodsBuffer = newStringBuffer();
	mainBuffer            = newStringBuffer();

	stringBufferAppend(mainBuffer, "; ------- Header --------------------------------------------"); 
	sprintf(tempString, ".class  public synchronized %s", className);
	stringBufferAppend(mainBuffer, tempString);
	stringBufferAppend(mainBuffer, ".super  java/lang/Object");
	stringBufferAppend(mainBuffer, "; -----------------------------------------------------------");
	stringBufferAppend(mainBuffer, "");
	
	stringBufferAppend(finishedMethodsBuffer, "; ------- Constructor ---------------------------------------");
	stringBufferAppend(finishedMethodsBuffer, ".method public <init>()V");
	stringBufferAppend(finishedMethodsBuffer, "\t.limit stack 1");
	stringBufferAppend(finishedMethodsBuffer, "\t.limit locals 1");
	stringBufferAppend(finishedMethodsBuffer, "\taload_0");
	stringBufferAppend(finishedMethodsBuffer, "\tinvokenonvirtual java/lang/Object/<init>()V");
	stringBufferAppend(finishedMethodsBuffer, "\treturn");
	stringBufferAppend(finishedMethodsBuffer, ".end method");
	stringBufferAppend(finishedMethodsBuffer, "; -----------------------------------------------------------");
	stringBufferAppend(finishedMethodsBuffer, "");

	stringBufferAppend(staticVariableBuffer, "; ------- Class Variables -----------------------------------");

	stringBufferAppend(classInitBuffer, "; ------- Class Initializer ---------------------------------");
	stringBufferAppend(classInitBuffer, ".method static <clinit>()V");
	classInitBufferIndex = classInitBuffer->numberOfNextElement;
	stringBufferAppend(classInitBuffer, "\t.limit locals 0");

}

void codegenAppendCommand(char* cmd, int stackdiff) {
	char tempString[MAX_LENGTH_OF_COMMAND];
	sprintf(tempString, "\t%s", cmd);
	if (global) stringBufferAppend(classInitBuffer, tempString);
	else stringBufferAppend(currentMethodBuffer, tempString);
	increaseStackby(stackdiff);
}

void codegenInsertCommand(int address, char* cmd, int stackdiff) {
	char tempString[MAX_LENGTH_OF_COMMAND];
	sprintf(tempString, "\t%s", cmd);
	if (global) stringBufferInsert(classInitBuffer, address, tempString);
	else stringBufferInsert(currentMethodBuffer, address, tempString);
	increaseStackby(stackdiff);
}

void codegenAppendLabel(int label) {
	char tempString[MAX_LENGTH_OF_COMMAND];
	sprintf(tempString, "Label%d:", label);
	if (global) stringBufferAppend(classInitBuffer, tempString);
	else stringBufferAppend(currentMethodBuffer, tempString);
}

void codegenAddVariable(char* name, int type) {
	/*fprintf(stderr, "add variable %s(%d) global=%d ", name, convertType(type), global);*/
	if (global) {
		if (type == TYPE_INT) sprintf(tempString, ".field static %s %c", name, 'I');
		else if (type == TYPE_FLOAT) sprintf(tempString, ".field static %s %c", name, 'F');
		else if (type == TYPE_BOOLEAN) sprintf(tempString, ".field static %s %c", name, 'Z');
		else yyerror("compiler-intern error in codegenAddGlobalVariable().\n");
		stringBufferAppend(staticVariableBuffer, tempString);
	}
	else {
		currentMethodNumberOfLocals++;
	}
}

int codegenGetNextLabel() {
	return labelCounter++;
}

int codegenGetCurrentAddress() {
	if (global) return classInitBuffer->numberOfNextElement;
	else return currentMethodBuffer->numberOfNextElement;
}

void codegenEnterFunction(symtabEntry* entry) {
	currentMethodBuffer = newStringBuffer();
	currentMethodStackSize = 0;
	currentMethodStackSizeMax = 0;
	labelCounter = 1;
	global = 0;
	
	if (strcmp(entry->name, "main") == 0) {
		if (entry->idtype != TYPE_VOID) yyerror("main has to be void.\n");
		currentMethodNumberOfLocals = 1;
		symtabInsert(strdup("#main-param#"), TYPE_VOID, CLASS_FUNC);
		stringBufferAppend(currentMethodBuffer, "; ------- Methode ---- void main() --------------------------");
		stringBufferAppend(currentMethodBuffer, ".method public static main([Ljava/lang/String;)V");
	}
	else {
		int i;
		currentMethodNumberOfLocals = entry->paramIndex;
		stringBufferAppend(currentMethodBuffer, "; ------- Methode -------------------------------------------");
		sprintf(tempString, ".method public static %s(", entry->name);
		for (i=entry->paramIndex-1; i>=0; i--) {
			int type = entry->params[i]->idtype;
			tempString[strlen(tempString)+1] = 0;
			tempString[strlen(tempString)] = convertType(type);
		}
		tempString[strlen(tempString)+2] = 0;
		tempString[strlen(tempString)+1] = convertType(entry->idtype);
		tempString[strlen(tempString)]   = ')';
		stringBufferAppend(currentMethodBuffer, tempString);
	}
	currentMethodBufferIndex = currentMethodBuffer->numberOfNextElement;
}

void codegenLeaveFunction() {
	global = 1;
	sprintf(tempString, "\t.limit locals %d", currentMethodNumberOfLocals);
	stringBufferInsert(currentMethodBuffer, currentMethodBufferIndex, tempString);
	sprintf(tempString, "\t.limit stack %d", currentMethodStackSizeMax);
	stringBufferInsert(currentMethodBuffer, currentMethodBufferIndex, tempString);
	stringBufferAppend(currentMethodBuffer, "\treturn");
	stringBufferAppend(currentMethodBuffer, ".end method");
	stringBufferAppend(currentMethodBuffer, "; -----------------------------------------------------------");
	stringBufferAppend(currentMethodBuffer, "");

	stringBufferConcatenate(finishedMethodsBuffer, currentMethodBuffer);
}



void codegenFinishCode() {
	stringBufferAppend(staticVariableBuffer, "; -----------------------------------------------------------");
	stringBufferAppend(staticVariableBuffer, "");

	sprintf(tempString, "\t.limit stack %d", classInitStackSizeMax);
	stringBufferInsert(classInitBuffer, classInitBufferIndex, tempString);
	stringBufferAppend(classInitBuffer, "\treturn");
	stringBufferAppend(classInitBuffer, ".end method");
	stringBufferAppend(classInitBuffer, "; -----------------------------------------------------------");
	
	stringBufferConcatenate(mainBuffer, staticVariableBuffer);
	stringBufferConcatenate(mainBuffer, finishedMethodsBuffer);
	stringBufferConcatenate(mainBuffer, classInitBuffer);

	stringBufferPrint(mainBuffer);
}

static void increaseStackby(int stackdiff) {
	if (global) {
		classInitStackSize += stackdiff;
		if (classInitStackSize > classInitStackSizeMax) classInitStackSizeMax = classInitStackSize;
	}
	else {
		currentMethodStackSize += stackdiff;
		if (currentMethodStackSize > currentMethodStackSizeMax) currentMethodStackSizeMax = currentMethodStackSize;
	}
}

char convertType(int type) {
	switch(type) {
		case TYPE_VOID:    return 'V';
		case TYPE_INT:     return 'I';
		case TYPE_FLOAT:   return 'F';
		case TYPE_BOOLEAN: return 'Z';
		default: yyerror("compiler-intern error in convertType().\n");
	}
	return 0; /* to avoid compiler-warning */
}


//#include <stdlib.h>
//#include <stdio.h>

int main() {
	int a = 12, b = 44;
	while (a != b) {
		if (a > b)
			a -= b;
		else
			b -= a;
	}
	printf("%d\n%d", a, 0X0);\
}


/**********************************************************************

  array.c -

  $Author: murphy $
  $Date: 2005-11-05 04:33:55 +0100 (Sa, 05 Nov 2005) $
  created at: Fri Aug  6 09:46:12 JST 1993

  Copyright (C) 1993-2003 Yukihiro Matsumoto
  Copyright (C) 2000  Network Applied Communication Laboratory, Inc.
  Copyright (C) 2000  Information-technology Promotion Agency, Japan

**********************************************************************/

#include "ruby.h"
#include "util.h"
#include "st.h"
#include "node.h"

VALUE rb_cArray, rb_cValues;

static ID id_cmp;

#define ARY_DEFAULT_SIZE 16


void
rb_mem_clear(mem, size)
    register VALUE *mem;
    register long size;
{
    while (size--) {
	*mem++ = Qnil;
    }
}

static inline void
memfill(mem, size, val)
    register VALUE *mem;
    register long size;
    register VALUE val;
{
    while (size--) {
	*mem++ = val;
    }
}

#define ARY_TMPLOCK  FL_USER1

static inline void
rb_ary_modify_check(ary)
    VALUE ary;
{
    if (OBJ_FROZEN(ary)) rb_error_frozen("array");
    if (FL_TEST(ary, ARY_TMPLOCK))
	rb_raise(rb_eRuntimeError, "can't modify array during iteration");
    if (!OBJ_TAINTED(ary) && rb_safe_level() >= 4)
	rb_raise(rb_eSecurityError, "Insecure: can't modify array");
}

static void
rb_ary_modify(ary)
    VALUE ary;
{
    VALUE *ptr;

    rb_ary_modify_check(ary);
    if (FL_TEST(ary, ELTS_SHARED)) {
	ptr = ALLOC_N(VALUE, RARRAY(ary)->len);
	FL_UNSET(ary, ELTS_SHARED);
	RARRAY(ary)->aux.capa = RARRAY(ary)->len;
	MEMCPY(ptr, RARRAY(ary)->ptr, VALUE, RARRAY(ary)->len);
	RARRAY(ary)->ptr = ptr;
    }
}

VALUE
rb_ary_freeze(ary)
    VALUE ary;
{
    return rb_obj_freeze(ary);
}
