#!/bin/bash

# Script para crear y configurar el repositorio en GitHub
# Autor: INSA Ingeniería
# Fecha: Noviembre 2025

echo "🚀 Creando repositorio ANH Reporter Showcase en Español..."

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuración
REPO_NAME="anh-reporter-showcase-es"
REPO_DESCRIPTION="Sistema Inteligente de Cumplimiento Regulatorio ANH - Telemetría Automatizada para la Industria Petrolera Colombiana 🇨🇴"
REPO_TOPICS="anh colombia oil-gas telemetry iot industrial-automation scada opc-ua rust python vue3 machine-learning compliance spanish"

echo -e "${YELLOW}📝 Inicializando repositorio Git local...${NC}"
git init

echo -e "${YELLOW}📄 Agregando archivos...${NC}"
git add .
git commit -m "feat: Initial commit - ANH Smart Reporter Showcase ES

- Comprehensive Spanish documentation
- ROI metrics and case studies
- Technical architecture diagrams
- Production-ready system showcase
- 99.98% uptime, 100K ops/sec performance"

echo -e "${YELLOW}🌐 Creando repositorio en GitHub...${NC}"
# Nota: Requiere GitHub CLI instalado y autenticado
gh repo create WilBtc/$REPO_NAME \
  --public \
  --description "$REPO_DESCRIPTION" \
  --homepage "https://insaingenieria.com/anh-reporter" \
  --license proprietary

echo -e "${YELLOW}🏷️ Agregando topics...${NC}"
for topic in $REPO_TOPICS; do
  gh repo edit WilBtc/$REPO_NAME --add-topic "$topic"
done

echo -e "${YELLOW}🔗 Conectando con repositorio remoto...${NC}"
git branch -M main
git remote add origin https://github.com/WilBtc/$REPO_NAME.git
git push -u origin main

echo -e "${YELLOW}📋 Configurando GitHub Pages (opcional)...${NC}"
gh repo edit WilBtc/$REPO_NAME --enable-pages --pages-source main --pages-path /docs

echo -e "${GREEN}✅ Repositorio creado exitosamente!${NC}"
echo ""
echo "🔗 URL: https://github.com/WilBtc/$REPO_NAME"
echo "📖 Docs: https://wilbtc.github.io/$REPO_NAME"
echo ""
echo "📊 Estadísticas del repositorio:"
echo "   - Archivos: $(find . -type f | wc -l)"
echo "   - Líneas de código: $(find . -name "*.md" -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "   - Tamaño: $(du -sh . | cut -f1)"
echo ""
echo "🎯 Próximos pasos:"
echo "   1. Revisar el repositorio en GitHub"
echo "   2. Configurar GitHub Actions para CI/CD"
echo "   3. Agregar colaboradores si es necesario"
echo "   4. Configurar webhooks para integraciones"
echo ""
echo "¡Gracias por usar ANH Smart Reporter! 🚀"