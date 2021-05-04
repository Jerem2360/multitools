#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#define PyObj static PyObject*


/*
* _c_maths functions:
*/

PyObj exp_(PyObject* module_, PyObject* args) {

    double x = 0.0;
    
    if (!PyArg_ParseTuple(args, "d", &x)) {
        return NULL;
    }

    return PyFloat_FromDouble(exp(x));
}


/*
* Class Complex():
*/

typedef struct {
    PyObject_HEAD
    double real;
    double imag;
} ComplexObject;

// Complex functions:

// ComplexType.conjugate() -> ComplexType
PyObj Complex_Conjugate(ComplexObject* self) {
    ComplexObject* result = self;
    result->imag = -result->imag;

    return result;
}



// Complex.__init__(self, real, imag):
static int
Complex_init(ComplexObject* self, PyObject* args)
{
    if (!PyArg_ParseTuple(args, "dd", &self->real, &self->imag)) {
        return NULL;
    };

    return 0;
}

// Complex.__repr__(self) -> str:
PyObj Complex_repr(ComplexObject* self) {
    return PyUnicode_FromFormat("%s+%pi", self->real, self->imag);
}


static PyMemberDef Complex_members[] = {

    {"real", T_FLOAT, offsetof(ComplexObject, real), 0,
     "The real part of a complex number"},
     {"imag", T_FLOAT, offsetof(ComplexObject, imag), 0,
     "The imaginary part of a complex number"},
    {NULL}  /* Sentinel */
};


static PyMethodDef Complex_methods[] = {
    // {name, c_function, flags, doc}
    {"conjugate", (PyCFunction)Complex_Conjugate, METH_NOARGS, "conjugate() -> complex \nReturn self, but conjugated."},
    {NULL}  /* Sentinel */
};

static PyTypeObject ComplexType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_c_math.ComplexType",
    .tp_doc = "A type representing complex numbers. ",
    .tp_basicsize = sizeof(ComplexObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)Complex_init,
    .tp_members = Complex_members,
    .tp_methods = Complex_methods,
    .tp_repr = (reprfunc)Complex_repr,
};




/*
* Class Infinite():
*/
typedef struct {
    PyObject_HEAD
    int pos;
} InfiniteObject;


// Infinite.invert() -> None :
PyObj Infinite_Invert(InfiniteObject* self) {
    if (self->pos == 0) {
        self->pos = 1;
    }
    else {
        self->pos = 0;
    }

    Py_RETURN_NONE;
}

// Infinite.__init__(self, positive):
static int
Infinite_init(InfiniteObject* self, PyObject* args)
{
    int positive;


    if (!PyArg_ParseTuple(args, "p", &positive)) {

        return NULL;
    };

    self->pos = positive;

    return 0;
}


static PyMemberDef Infinite_members[] = {
    
    {"pos", T_BOOL, offsetof(InfiniteObject, pos), 0,
     "Whether value is +infinite."},
    {NULL}  /* Sentinel */
};


static PyMethodDef Infinite_methods[] = {
    {"invert", (PyCFunction)Infinite_Invert, METH_NOARGS,
    "InfiniteType.invert() -> None\n Invert the infinite's sign."
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject InfiniteType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_c_math.InfiniteType",
    .tp_doc = "A type representing simple infinite values. ",
    .tp_basicsize = sizeof(InfiniteObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)Infinite_init,
    .tp_members = Infinite_members,
    .tp_methods = Infinite_methods,

};

// build the methods of _c_maths:
static PyMethodDef _c_math_functions[] = {
    // {method_name, method, flags, doc},
    {"exp", (PyCFunction)exp_, METH_VARARGS, "exp(x: float) -> float \nReturn the image of x by the exponential function."},
    {NULL, NULL, 0, NULL},
};


static PyModuleDef _c_math = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_c_maths",
    .m_doc = "An extension made in C that implements simple math functions and types.",
    .m_size = -1,
    .m_methods = _c_math_functions,
};

PyMODINIT_FUNC
PyInit__c_maths(void)
{
    PyObject* m;
    if (PyType_Ready(&InfiniteType) < 0)
        return NULL;

    if (PyType_Ready(&ComplexType) < 0)
        return NULL;

    m = PyModule_Create(&_c_math);

    ComplexObject* i;
    
    i->imag = 1;
    i->real = 0;

    PyModule_AddObject(m, "e", PyFloat_FromDouble(exp(1)));
    PyModule_AddObject(m, "i", i);

    if (m == NULL)
        return NULL;

    Py_INCREF(&InfiniteType);
    if (PyModule_AddObject(m, "InfiniteType", (PyObject*)&InfiniteType) < 0) {
        Py_DECREF(&InfiniteType);
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(&ComplexType);
    if (PyModule_AddObject(m, "ComplexType", (PyObject*)&ComplexType) < 0) {
        Py_DECREF(&ComplexType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
