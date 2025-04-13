# AI-Agent-Columnist

**AI-Agent-Columnist** is a Repository designed to generate HBR-style articles using Storm [Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking (STORM)] framework and Langchain tool. It provides tools to automatically create outlines, expand on topics, generate expert perspectives, and manage expert conversations—resulting in high-quality, well-structured content.

## Key Features
- **Initial Outline Generation:** Automatically create a draft outline from a given topic.
- **Topic Expansion:** Identify and propose related subjects to ensure a diverse range of perspectives.
- **Expert Perspective Generation:** Select and simulate input from domain experts to add depth and credibility.
- **Conversation Management:** Facilitate dialogs between a “Wikipedia Editor” and a “Domain Expert” to refine content.
- **Integrated Search Engine:** Leverage web search capabilities to retrieve references and validate information.

## Project Structure

```
AI-Agent-Columnist/
├── Dialog_Roles.py            # Manages conversation roles and flow between participants.
├── Expand_Topics.py           # Expands the given topic into related subjects.
├── Expert_Dialog.py           # Handles dialogs between experts for a refined article outline.
├── Gen_Initial_Outline.py     # Generates an initial article outline based on the topic.
├── Gen_Perspectives.py        # Generates expert perspectives and editor personas.
├── Interview_State.py         # Stores conversation states, messages, and references.
├── search_engine.py           # Integrates a web search engine for data and citation retrieval.
├── Setup.py                   # Basic configuration settings for the project.
├── Utils.py                   # Utility functions and message routing.
└── README.md                  # This file.
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your_username/AI-Agent-Columnist.git
   cd AI-Agent-Columnist
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/MacOS
   venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *Note: If you haven't created a `requirements.txt` file yet, ensure you list all necessary dependencies such as `langchain_core`, `pydantic`, `langchain_community`, etc.*

## Usage

### Generating an Initial Outline
Use the `Gen_Initial_Outline.py` module to generate a draft outline for your article. For example:

```python
from Gen_Initial_Outline import GenInitialOutline, Outline, Section, Subsection

# Define or mock your LLM instances (or use your actual LLMs)
class MockLLM:
    def with_structured_output(self, schema):
        return self
    def invoke(self, prompt):
        return Outline(
            page_title="Demo Page",
            sections=[
                Section(
                    section_title="Introduction",
                    description="An introductory section.",
                    subsections=[
                        Subsection(subsection_title="Background", description="Details about the background...")
                    ]
                )
            ]
        )

fast_llm = MockLLM()
long_context_llm = MockLLM()

generator = GenInitialOutline(fast_llm=fast_llm, long_context_llm=long_context_llm)
outline = generator.generate_outline("A Topic of Interest", use_long_context=False)
print(outline.as_str)
```

### Expanding Topics and Generating Perspectives
- **Topic Expansion:** Utilize `Expand_Topics.py` to propose related subjects for a given topic.
- **Expert Perspectives:** Use `Gen_Perspectives.py` to simulate expert input and generate various editorial perspectives.

### Conversation Management
Modules like `Dialog_Roles.py` and `Interview_State.py` are used to manage dialogs and maintain a history of interactions between the roles within the system.

### Web Search Integration
The `search_engine.py` module enables fetching real-time references and data from the internet to support accurate and well-cited content.

## Contributing
- To contribute, please fork this repository and submit pull requests.
- For bug reports or feature suggestions, create a new issue on GitHub.

## License
This project is licensed under the MIT License (or another license of your choice). Please see the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries or further information, you can reach me at [Nutdnuy@Gmail.com](mailto:Nutdnuy@Gmail.com).

---

This README.md provides a comprehensive overview of your project, including its functionality, directory structure, installation, and usage instructions. Feel free to modify and expand the content to suit your project’s specifics and any additional features you plan to implement.
```

---

You can adjust the contents as needed. If you have further questions or need more assistance, feel free to ask!
