# Q6 Autopsy quick guide

1. Obtain the actual instructor image/evidence set.
2. Record evidence ID, source, acquisition method/date, file size, and custody notes.
3. Preserve the original read-only; analyze a working copy.
4. Calculate SHA-256 before and after copying:

```bash
sha256sum /path/to/evidence.E01
stat /path/to/evidence.E01
file /path/to/evidence.E01
```

5. In Autopsy, create a case, select **Add Data Source**, and add the supplied image.
6. Enable applicable ingest modules: file type identification, hash calculation/lookup if configured, keyword search, recent activity/web artifacts, EXIF parsing, and metadata analysis.
7. Review browser history/downloads, recent files, deleted files, archives, executables, relevant logs, and metadata.
8. Open Timeline; record timezone and source for every timestamp.
9. Bookmark relevant artifacts, export a report, and hash exported evidence when appropriate.

Do not invent file names, hashes, timestamps, or incident findings. If the evidence was not supplied, state that analysis is pending.

Official illustrative UI references (not case evidence):
- https://sleuthkit.org/autopsy/docs/user-docs/4.12.0/quick_start_guide.html
- https://sleuthkit.org/autopsy/docs/user-docs/4.21.0/ingest_page.html
- https://sleuthkit.org/autopsy/docs/user-docs/4.16.0/timeline_page.html
