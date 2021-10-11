import os
from fppy import __version__

def docs():
    """生成DOC
    """
    build_dir = 'docs/build/'+ __version__
    source_dir = 'docs/source'
    build_main_dir = 'docs/build/main'
    os.system((
        f'sphinx-build -b html {source_dir} {build_dir}'
        ))
    os.system((
        f'sphinx-build -b html {source_dir} {build_main_dir}'
        ))

def test_with_badge():
    """运行测试

    Examples:
        ```python
        ## 在代码行种使用如下命令即可执行测试
        poetry run test
        ```
    """
    os.system((
        'pytest '
        '--html=dist/report.html '
        '--cov-report html:cov_html '
        '--cov-report xml:cov.xml '
        '--cov-report annotate:cov_annotate '
        '--cov-report= '
        '--cov=fppy '
        'tests/'))
    if os.path.isfile('badge/cov-badge.svg'):
        os.remove('badge/cov-badge.svg')
    os.system('coverage-badge -o badge/cov-badge.svg')

if __name__ == "__main__":
    docs()
    test_with_badge()