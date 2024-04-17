# 设置相对路径
relative_path="rarlib/libunrar.so"

# 获取绝对路径
absolute_path="$(pwd)/$relative_path"

# 检查文件是否存在
if [ -f "$absolute_path" ]; then
    # 将路径添加到用户的 .bashrc 文件中
    echo "export UNRAR_LIB_PATH=$absolute_path" >> ~/.bashrc
    # 使环境变量立即生效
    source ~/.bashrc
    echo "已成功设置 UNRAR_LIB_PATH 环境变量为：$absolute_path"
else
    echo "文件 $absolute_path 不存在，请确保路径正确。"
fi