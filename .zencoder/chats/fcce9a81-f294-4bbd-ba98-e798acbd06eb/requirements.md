# Product Requirements Document (PRD)

## Overview
**Datei Checker** is a file recovery and restoration tool that automatically detects file types from binary signatures (magic bytes) and restores file extensions and original filenames to corrupted or stripped files.

## Problem Statement
Users have recovered data files that have lost their file extensions and original names. The file type information exists in the file's binary content but is not visible without a hex editor. Manual identification and renaming of hundreds of files is inefficient.

## User Goals
1. Quickly identify and restore file extensions for recovered files
2. Restore original filenames when available in file metadata
3. Process entire directory structures (including subdirectories) in batch
4. Both programmatic (CLI) and interactive (GUI) access to the tool

## Functional Requirements

### Core Features
1. **File Type Detection**
   - Scan files for magic bytes (file signatures) to identify type
   - Support extended list of file types including:
     - Documents (PDF, Office formats, etc.)
     - Images (JPG, PNG, GIF, BMP, etc.)
     - Archives (ZIP, RAR, 7Z, etc.)
     - Video/Audio (MP4, MKV, MP3, WAV, etc.)
     - Databases (SQLite, etc.)
     - Other common binary formats
   - Handle unknown file types gracefully

2. **Filename Restoration**
   - Extract original filenames from file metadata when available
   - Examples:
     - JPEG EXIF data (original filename in metadata)
     - PDF metadata (Title, Subject fields)
     - Archive file headers
   - Fall back to extension-based naming if metadata unavailable

3. **Batch Processing**
   - Accept directory path via GUI folder picker or CLI argument
   - Recursively process all subdirectories
   - Rename files in-place
   - Maintain directory structure

4. **User Interfaces**
   - **GUI Application**: 
     - Folder selection dialog
     - Progress indicator for batch processing
     - Log/preview of changes before committing
     - Result summary
   - **CLI Application**:
     - Accept directory path as argument
     - Verbose/quiet modes
     - Dry-run option
     - Output results to console/file

### Non-Functional Requirements
1. Reliable file type identification (magic bytes)
2. Safe file handling (no data corruption)
3. Performance: process large directory structures efficiently
4. Error handling: graceful failures for unreadable files or permission issues
5. Rollback capability or clear logging for debugging

## Out of Scope
- Network file locations (initially local filesystem only)
- Real-time monitoring of file changes
- Custom magic byte definitions (hardcoded list)
- File content repair or reconstruction

## Success Criteria
- Successfully identify and rename 95%+ of recovered files
- Process 1000+ files in reasonable time
- No file data corruption during renaming
- Both GUI and CLI interfaces functional and usable

## Technology Recommendations
Given no language preference:
- **Python** recommended for speed of development, extensive file handling libraries, cross-platform support
- Alternative: C# for Windows-focused GUI, .NET has good file APIs
