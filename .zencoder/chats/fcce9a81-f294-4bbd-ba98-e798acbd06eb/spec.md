# Technical Specification (Revised for Python Performance)

## Technology Stack Selection

**Primary Language: Python 3.12+**
- **Performance Strategy**: 
  - Use `asyncio` for non-blocking I/O operations.
  - Use `ProcessPoolExecutor` for CPU-bound magic byte detection and metadata extraction to bypass the GIL.
  - Highly optimized standard library for file operations.
  - **Estimated Performance**: 500-1000 files/second (sufficient for "thousands" of files).

**GUI Layer: CustomTkinter / Tkinter**
- Modern, fast, and native look for Windows.
- Simple integration with the same Python codebase.

## Architecture

### Component Structure

```
datei_checker/
├── core/
│   ├── detector.py      # Magic byte detection logic
│   ├── metadata.py      # Metadata extraction (EXIF, PDF, ZIP)
│   ├── renamer.py       # Safe renaming logic
│   └── processor.py     # Concurrent directory processing
├── ui/
│   ├── app.py           # GUI implementation (CustomTkinter)
│   └── cli.py           # CLI implementation
└── main.py              # Unified entry point
```

### Performance Optimizations

1. **Multiprocessing**: Utilize all CPU cores for file signature analysis.
2. **Batch I/O**: Read only required headers (first 2-4KB).
3. **Memory Efficiency**: Use generators for file discovery.

## Implementation Approach

### Phase 1: Core Logic
1. Magic byte database for extended list of types.
2. Safe renaming engine (dry-run, conflict handling).
3. Concurrent processor (ProcessPoolExecutor).

### Phase 2: Metadata Extraction
1. JPEG/PNG metadata.
2. PDF/Office document properties.
3. Archive header analysis.

### Phase 3: Interfaces
1. CLI with rich progress bars.
2. GUI with modern folder picker and status view.

### Phase 4: Final Testing
1. Integration test with 1000+ files.
2. Binary distribution (PyInstaller).
