#!/bin/bash

# F1 Analytics Platform - Validation Script
echo "🔍 F1 Analytics Platform Validation"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

# Test function
test_requirement() {
  local name=$1
  local command=$2

  if eval "$command" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} $name"
    ((PASS++))
  else
    echo -e "${RED}✗${NC} $name"
    ((FAIL++))
  fi
}

echo "📋 Environment & Dependencies:"
test_requirement "Node.js installed" "node --version"
test_requirement "npm installed" "npm --version"
test_requirement "Python installed" "python --version"
test_requirement "Docker installed" "docker --version"

echo ""
echo "📁 Project Structure:"
test_requirement "api/ directory exists" "test -d api"
test_requirement "frontend/ directory exists" "test -d frontend"
test_requirement "pipeline/ directory exists" "test -d pipeline"

echo ""
echo "⚙️  Configuration Files:"
test_requirement ".env file exists" "test -f .env"
test_requirement ".env.example exists" "test -f .env.example"
test_requirement "docker-compose.yml exists" "test -f docker-compose.yml"

echo ""
echo "🐳 Docker Configuration:"
test_requirement "api/Dockerfile exists" "test -f api/Dockerfile"
test_requirement "frontend/Dockerfile exists" "test -f frontend/Dockerfile"
test_requirement "pipeline/Dockerfile exists" "test -f pipeline/Dockerfile"

echo ""
echo "📦 API Files:"
test_requirement "api/package.json exists" "test -f api/package.json"
test_requirement "api/src/index.js exists" "test -f api/src/index.js"
test_requirement "api/src/db.js exists" "test -f api/src/db.js"
test_requirement "api routes configured" "test -d api/src/routes"

echo ""
echo "🎨 Frontend Files:"
test_requirement "frontend/package.json exists" "test -f frontend/package.json"
test_requirement "frontend/src/app/page.js exists" "test -f frontend/src/app/page.js"
test_requirement "frontend/src/app/layout.js exists" "test -f frontend/src/app/layout.js"
test_requirement "frontend components exist" "test -d frontend/src/components"

echo ""
echo "🔧 Pipeline Files:"
test_requirement "pipeline/requirements.txt exists" "test -f pipeline/requirements.txt"
test_requirement "pipeline/src/main.py exists" "test -f pipeline/src/main.py"
test_requirement "pipeline/src/database/schema.sql exists" "test -f pipeline/src/database/schema.sql"

echo ""
echo "=================================="
echo -e "Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"

if [ $FAIL -eq 0 ]; then
  echo -e "${GREEN}✅ All validations passed!${NC}"
  echo ""
  echo "Next steps:"
  echo "1. Update .env with your configuration"
  echo "2. Run: docker-compose up --build"
  echo "3. Visit http://localhost:3000"
  exit 0
else
  echo -e "${RED}❌ Some validations failed${NC}"
  exit 1
fi
