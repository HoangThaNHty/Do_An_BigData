package vn.huit.realestate;

import java.io.IOException;
import java.io.FileNotFoundException;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Stream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.RawLocalFileSystem;
import org.apache.hadoop.fs.LocalFileSystem;
import org.apache.hadoop.fs.permission.FsPermission;

/** Local Windows adapter: Java NIO IO, inherited Windows ACLs, no POSIX chmod.
 * Used only for this project's file:// experiment, never for HDFS/cluster IO.
 */
public final class ProjectLocalFileSystem extends LocalFileSystem {
    public ProjectLocalFileSystem() {
        super(new ProjectRawLocalFileSystem());
        setVerifyChecksum(false);
        setWriteChecksum(false);
    }
}

final class ProjectRawLocalFileSystem extends RawLocalFileSystem {
    @Override public void setPermission(Path path, FsPermission ignored) throws IOException {
        if (!Files.exists(pathToFile(path).toPath())) throw new FileNotFoundException(path.toString());
        // Windows ACLs remain inherited; POSIX permission bits are not implemented.
    }

    @Override public boolean mkdirs(Path path, FsPermission permission) throws IOException {
        Files.createDirectories(pathToFile(path).toPath());
        return true;
    }

    @Override public FileStatus getFileStatus(Path path) throws IOException {
        java.nio.file.Path local = pathToFile(path).toPath();
        if (!Files.exists(local)) throw new FileNotFoundException(path.toString());
        BasicFileAttributes a = Files.readAttributes(local, BasicFileAttributes.class);
        return new FileStatus(a.size(), a.isDirectory(), 1, getDefaultBlockSize(path),
            a.lastModifiedTime().toMillis(), a.lastAccessTime().toMillis(),
            FsPermission.getDefault(), System.getProperty("user.name"), "", path.makeQualified(getUri(), getWorkingDirectory()));
    }

    @Override public FileStatus[] listStatus(Path path) throws IOException {
        FileStatus status = getFileStatus(path);
        if (!status.isDirectory()) return new FileStatus[] {status};
        List<FileStatus> result = new ArrayList<>();
        try (Stream<java.nio.file.Path> entries = Files.list(pathToFile(path).toPath())) {
            for (java.nio.file.Path entry : (Iterable<java.nio.file.Path>) entries::iterator)
                // NIO directory URIs end in '/'. Hadoop's URI constructor keeps
                // that slash, making getName() empty during partition commits.
                result.add(getFileStatus(new Path(path, entry.getFileName().toString())));
        }
        return result.toArray(new FileStatus[0]);
    }

    @Override public boolean rename(Path source, Path target) throws IOException {
        java.nio.file.Path from = pathToFile(source).toPath();
        java.nio.file.Path to = pathToFile(target).toPath();
        if (!Files.exists(from)) return false;
        if (Files.isDirectory(to)) to = to.resolve(from.getFileName());
        if (Files.exists(to)) return false;
        Files.move(from, to);
        return true;
    }

    @Override public boolean delete(Path path, boolean recursive) throws IOException {
        java.nio.file.Path local = pathToFile(path).toPath().toAbsolutePath().normalize();
        if (!Files.exists(local, LinkOption.NOFOLLOW_LINKS)) return false;
        String rootValue = System.getenv("REAL_ESTATE_ROOT");
        if (rootValue == null) throw new IOException("REAL_ESTATE_ROOT required for local deletion");
        java.nio.file.Path root = java.nio.file.Paths.get(rootValue).toAbsolutePath().normalize();
        // Spark may replace only generated output/scratch files, never raw data or sources.
        boolean generated = local.startsWith(root.resolve(".runtime"))
            || local.startsWith(root.resolve("data/processed"))
            || local.startsWith(root.resolve("artifacts"));
        if (!generated || local.equals(root)) throw new IOException("Deletion outside generated project paths: " + local);
        if (!Files.isDirectory(local, LinkOption.NOFOLLOW_LINKS) || !recursive) {
            Files.delete(local);
        } else {
            try (Stream<java.nio.file.Path> entries = Files.walk(local)) {
                for (java.nio.file.Path entry : (Iterable<java.nio.file.Path>) entries.sorted(Comparator.reverseOrder())::iterator)
                    Files.delete(entry);
            }
        }
        return true;
    }
}
