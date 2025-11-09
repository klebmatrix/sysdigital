#!/bin/bash
# Instala aiohttp explicitamente para contornar problemas de cache/dependência do Render
pip install aiohttp

# Inicia a aplicação
gunicorn main:app

