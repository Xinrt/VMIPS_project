$origin_files = @("C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\origin_op\SDMEM.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\origin_op\SDMEMOP.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\origin_op\SRF.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\origin_op\VDMEM.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\origin_op\VDMEMOP.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\origin_op\VRF.txt")
$new_files = @("C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\SDMEM.txt", 
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\SDMEMOP.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\SRF.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\VDMEM.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\VDMEMOP.txt",
"C:\Users\xiang\Documents\2023Spring\9413\VMIPS_project\sample\dot_product_test\VRF.txt")

$file_origin = Get-ChildItem $origin_files | Select-Object -ExpandProperty FullName 
$file_new = Get-ChildItem $new_files | Select-Object -ExpandProperty FullName
$diff = Compare-Object (Get-Content $file_origin) (Get-Content $file_new) -PassThru | Select-Object -Unique

foreach ($file in $diff) {
    $filename = Split-Path $file -Leaf
    Write-Host "File $filename differs."
}
