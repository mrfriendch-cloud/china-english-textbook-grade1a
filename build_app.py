"""
CLI Entry Point for textbook app builder.
Delegates document assembly to the deep builder package.
"""
from builder import build_app

if __name__ == '__main__':
    build_app()