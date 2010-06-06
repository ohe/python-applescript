/**
* Copyright (c) 2009 Olivier Hervieu <olivier.hervieu@gmail.com>
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
* 
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
* 
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
**/

#include "python_applescript.h"

#define ADD_METHOD(method_name)\
    {#method_name,applescript_##method_name, METH_VARARGS, applescript_##method_name##_doc}

static PyObject  * applescriptException = NULL;

static PyMethodDef applescriptMethods[] = 
{
    ADD_METHOD(launch_script),
    {NULL, NULL} /* Sentinel */
};


char applescript_launch_script_doc[] = "launch_script(script)";
/* {{{ applescript_launch_script
*/
PyObject * 
applescript_launch_script(PyObject *obj, PyObject *args) {

    ComponentInstance theComponent = NULL;
    AEDesc scriptTextDesc;
    AEDesc resultData;
    OSStatus err = noErr;
    OSAID scriptID = kOSANullScript;
    OSAID resultID;

    int isError      = 0;
    char *text       = NULL;
    int returnSize   = 0;

    PyObject *buffer = NULL;

    /* Grep python args */
    if (PyArg_ParseTuple(args, "s", &text)){

        /* String convertion */
        err = AECreateDesc(typeUTF8Text, text, strlen(text), & scriptTextDesc);
        /* Open the scripting component */
        theComponent = OpenDefaultComponent(kOSAComponentType, typeAppleScript);

        /* Compile the script */
        err = OSACompile(theComponent, &scriptTextDesc, kOSAModeNull, &scriptID);
        if ( err == noErr) {
            /* Launch the script */ 
            err = OSAExecute(theComponent, scriptID, kOSANullScript, kOSAModeNull, &resultID);
            if (err != noErr) {
                isError = 1;
                AECreateDesc (typeNull, NULL, 0, &resultData);
                if (err == errOSAScriptError) {
                    OSAScriptError( theComponent, kOSAErrorMessage, typeUTF8Text, &resultData);
                }
            }
            else {
                AECreateDesc (typeNull, NULL, 0, &resultData);
                if (err ==noErr && resultID != kOSANullScript) {
                    OSADisplay (theComponent, resultID, typeUTF8Text, kOSAModeNull, &resultData);
                }
            };
            /* Yourey! There's something in resultData */
            returnSize = AEGetDescDataSize(&resultData);
            buffer = PyString_FromStringAndSize(NULL, returnSize);
            err = AEGetDescData(&resultData, PyString_AsString(buffer), returnSize);
            AEDisposeDesc(&resultData);
            if (isError) {
                PyErr_SetString(applescriptException, PyString_AsString(buffer));
                buffer = NULL;
            }
        }
        else {
            PyErr_SetString(applescriptException, "Failed to Compile given script");
            return NULL;
        }
    }
    else {
        PyErr_SetString(applescriptException, "Error Parsing args");
    }
    return buffer;
}
/* }}}*/

/* {{{ initapplescript
*/
void initapplescript(void) {

    PyObject *dict = NULL;
    PyObject *mod  = NULL;

    applescriptException = PyErr_NewException("applescript.Error", NULL, NULL);

    mod = Py_InitModule3(
            "applescript",      /* name of the module       */
            applescriptMethods, /* name of the method table */
            "Python extension to execute applescript commands on OS X"
        );

    dict = PyModule_GetDict(mod);
    PyDict_SetItemString(dict,"AppleScriptError",applescriptException);

    return;
}
/* }}} */
