@echo off
conda activate VMIPS
for /L %%i in (1,1,24) do (
    python xt2191_tx701_funcsimulator.py --iodir "sample\test%%i"
    echo Done Test%%i
)
