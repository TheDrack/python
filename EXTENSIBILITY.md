# Extensibility Guide

This guide explains how to extend Jarvis Assistant with new functionality.

## Adding New Commands

### 1. Create a New Action Module

Create a new file in `app/actions/` for your functionality:

```python
# app/actions/my_new_feature.py
from typing import Optional

class MyNewFeature:
    """Handler for my new feature"""
    
    def __init__(self) -> None:
        """Initialize the feature"""
        pass
    
    def execute(self, param: str) -> Optional[str]:
        """
        Execute the feature
        
        Args:
            param: Command parameter
            
        Returns:
            Result message or None
        """
        # Your implementation here
        return "Feature executed"
```

### 2. Register Commands

Update `app/actions/system_commands.py` to include your new feature:

```python
from app.actions.my_new_feature import MyNewFeature

class CommandProcessor:
    def __init__(self, system_commands, web_navigator):
        self.sys_cmd = system_commands
        self.web_nav = web_navigator
        self.my_feature = MyNewFeature()  # Add your feature
        
        self.commands_map = {
            'escreva': self._handle_type,
            'my_command': self._handle_my_feature,  # Add mapping
        }
    
    def _handle_my_feature(self, param: str) -> None:
        """Handle my new feature"""
        result = self.my_feature.execute(param)
        print(result)
```

## Integrating AI Models (Snake)

To integrate AI models like Snake:

### 1. Create AI Module

```python
# app/actions/ai_integration.py
from typing import Any, Dict

class AIProcessor:
    """AI model integration"""
    
    def __init__(self, model_path: str) -> None:
        """
        Initialize AI processor
        
        Args:
            model_path: Path to AI model
        """
        self.model = self._load_model(model_path)
    
    def _load_model(self, path: str) -> Any:
        """Load the AI model"""
        # Your model loading logic
        pass
    
    def predict(self, input_data: Dict) -> Dict:
        """
        Make prediction
        
        Args:
            input_data: Input for the model
            
        Returns:
            Prediction results
        """
        # Your prediction logic
        return {}
```

### 2. Add AI Commands

```python
# In CommandProcessor
self.ai_processor = AIProcessor("path/to/model")

self.commands_map['prever'] = self._handle_prediction

def _handle_prediction(self, input_text: str) -> None:
    """Handle AI prediction"""
    result = self.ai_processor.predict({'text': input_text})
    self.engine.speak(f"Resultado: {result}")
```

## Web Scraping Integration

To add web scraping functionality:

### 1. Create Scraping Module

```python
# app/actions/web_scraper.py
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

class WebScraper:
    """Web scraping handler"""
    
    def __init__(self) -> None:
        """Initialize web scraper"""
        self.session = requests.Session()
    
    def scrape_page(self, url: str, selector: str) -> List[str]:
        """
        Scrape data from a web page
        
        Args:
            url: URL to scrape
            selector: CSS selector for data
            
        Returns:
            List of scraped data
        """
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        elements = soup.select(selector)
        return [elem.text for elem in elements]
```

### 2. Add to Command Processor

```python
from app.actions.web_scraper import WebScraper

self.scraper = WebScraper()
self.commands_map['extrair'] = self._handle_scrape

def _handle_scrape(self, command: str) -> None:
    """Handle web scraping"""
    # Parse command for URL and selector
    url, selector = self._parse_scrape_command(command)
    data = self.scraper.scrape_page(url, selector)
    self.engine.speak(f"Encontrei {len(data)} itens")
```

## Adding Custom DAGs

Create new Airflow DAGs in the `dags/` directory:

```python
# dags/my_custom_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def my_task():
    """Task implementation"""
    from app.core.engine import JarvisEngine
    # Use Jarvis functionality
    pass

dag = DAG(
    'my_custom_workflow',
    default_args={'start_date': datetime(2024, 1, 1)},
    schedule_interval=timedelta(days=1),
)

task = PythonOperator(
    task_id='my_task',
    python_callable=my_task,
    dag=dag,
)
```

## Testing New Features

Always add tests for new features:

```python
# tests/test_my_feature.py
import pytest
from app.actions.my_new_feature import MyNewFeature

class TestMyNewFeature:
    def test_execute(self):
        """Test feature execution"""
        feature = MyNewFeature()
        result = feature.execute("test")
        assert result is not None
```

## Configuration

Add new configuration options in `app/core/config.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Your new settings
    my_feature_enabled: bool = True
    my_api_key: Optional[str] = None
```

## Best Practices

1. **Type Hints**: Always use type hints
2. **Documentation**: Add docstrings to all public methods
3. **Testing**: Write tests for new functionality
4. **Modularity**: Keep modules focused and independent
5. **Configuration**: Use the Settings class for configuration
6. **Logging**: Use the logging utilities from `app/utils/helpers.py`
