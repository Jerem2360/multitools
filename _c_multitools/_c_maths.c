#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"


// implement an "infinite" type:

typedef struct {
    PyObject_HEAD


    /* Type-specific fields go here. */
    int pos;


} InfiniteObject;


PyObject* CustomRepr(PyObject* self) {
    return PyUnicode_FromString("Hello");
}


static PyTypeObject InfiniteType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_c_maths.infinite",
    .tp_doc = "A type that represents infinity.",
    .tp_basicsize = sizeof(InfiniteObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_repr = CustomRepr,
};



/*
 * Implement __doc__ for all extension functions:
 */

PyDoc_STRVAR(exp__doc, "Return exp(number). \nnumber must be a float.\n exp(number: float) -> float");

PyDoc_STRVAR(pow__doc, "Return x raised to the power of n.\n x is a real number, while n must be an integer.\n power(x: float, n: int) -> float");

PyDoc_STRVAR(root_doc, "Return x raised to the power of 1 / n; or the n-th root of x.\n x is a real number, while n must be an integer.\n root(x: float, n: int) -> float");


// exp(number: float) -> float
PyObject *exp_(PyObject *self, PyObject *args) {
    /* Shared references that do not need Py_DECREF before returning. */
    double number;
    PyObject* result;

    /* Parse positional arguments */
    if (!PyArg_ParseTuple(args, "d", &number)) {
        return NULL;
    }

    /* Function implementation starts here */

    result = PyLong_FromDouble(exp(number));

    return result;  // return exp(number)
}

// power(x: float, n: int) -> float
PyObject* power_(PyObject* self, PyObject* args) {
    double x;
    double n;

    // parse python arguments:
    if (!PyArg_ParseTuple(args, "di", &x, &n)) {
        return NULL;
    };

    // return pow(x, n):

    double result;

    result = pow(x, n);

    return PyLong_FromDouble(result);
}

// root(x: float, n: int) -> float
PyObject* root(PyObject* self, PyObject* args) {
    double x = 0.0;
    double n = 0.0;

    if (!PyArg_ParseTuple(args, "di", &x, &n)) {
        return NULL;
    };

    return PyLong_FromDouble(pow(x, 1 / n));
}

/*
 * List of functions to add to _c_maths in exec__c_maths().
 */
static PyMethodDef _c_maths_functions[] = {
    { "exp", (PyCFunction)exp_, METH_VARARGS, exp__doc },
    { "power", (PyCFunction)power_, METH_VARARGS, pow__doc },
    { "root", (PyCFunction)root, METH_VARARGS, root_doc },
    { NULL, NULL, 0, NULL } /* marks end of array */
};

/*
 * Initialize _c_maths. May be called multiple times, so avoid
 * using static state.
 */
int exec__c_maths(PyObject *module_) {
    PyModule_AddFunctions(module_, _c_maths_functions);

    PyModule_AddType(module_, &InfiniteType);

    PyModule_AddStringConstant(module_, "__author__", "Jerem");
    PyModule_AddStringConstant(module_, "__version__", "1.0.0");
    PyModule_AddIntConstant(module_, "year", 2021);
    PyModule_AddIntConstant(module_, "e", exp(1));

    return 0; /* success */
}

/*
 * Documentation for _c_maths.
 */
PyDoc_STRVAR(_c_maths_doc, "Simple maths module directly made from c. Only for internal use.");


static PyModuleDef_Slot _c_maths_slots[] = {
    { Py_mod_exec, exec__c_maths },
    { 0, NULL }
};

static PyModuleDef _c_maths_def = {
    PyModuleDef_HEAD_INIT,
    "_c_maths",
    _c_maths_doc,
    0,              /* m_size */
    NULL,           /* m_methods */
    _c_maths_slots,
    NULL,           /* m_traverse */
    NULL,           /* m_clear */
    NULL,           /* m_free */
};

PyMODINIT_FUNC PyInit__c_maths() {
    return PyModuleDef_Init(&_c_maths_def);
}
