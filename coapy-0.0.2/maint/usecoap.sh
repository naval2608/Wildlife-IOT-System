COAPY_ROOT=${COAPY_ROOT:-/home/pab/coapy/dev}
PYTHONPATH=${COAPY_ROOT}:${PYTHONPATH:+:${PYTHONPATH}}
PATH="${COAPY_ROOT}/scripts:${COAPY_ROOT}/bin:${PATH}"
export COAPY_ROOT PYTHONPATH PATH
