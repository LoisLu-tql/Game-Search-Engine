package cn.loix.test;

import cn.loix.dao.GameDao;
import cn.loix.dao.GameDaoImpl;
import cn.loix.pojo.Game;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.junit.Test;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class TestIndex {
    @Test
    public void creatIndexLibTest() throws Exception {
        GameDao gameDao = new GameDaoImpl();
        List<Game> gameList = gameDao.queryGameList();

        List<Document> documentList = new ArrayList<>();

        for(Game game : gameList){
            Document document = new Document();

            //不分词 不索引 存储
            document.add(new StoredField("game_img", game.getGame_img()));
            document.add(new StoredField("game_link", game.getGame_link()));
            //分词 索引 存储
            document.add(new TextField("game_name", game.getGame_name(), Field.Store.YES));
            document.add(new TextField("game_intro", game.getGame_intro(), Field.Store.YES));
            document.add(new TextField("game_tag", game.getGame_tag(), Field.Store.YES));
            //不分词 索引 存储
            document.add(new StringField("game_src", game.getGame_src(), Field.Store.YES));
            document.add(new StringField("id", String.valueOf(game.getId()), Field.Store.YES));
            document.add(new StringField("game_birth", game.getGame_birth(), Field.Store.YES));
            document.add(new StringField("game_developer", game.getGame_developer(), Field.Store.YES));
            document.add(new StringField("game_publisher", game.getGame_publisher(), Field.Store.YES));

            documentList.add(document);
        }

        Analyzer analyzer = new IKAnalyzer();
        Directory directory = FSDirectory.open(Paths.get("../indexlib"));

        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        IndexWriter indexWriter = new IndexWriter(directory, config);
//        indexWriter.forceMerge(1000);

        for(Document document : documentList){
            indexWriter.addDocument(document);
        }

        indexWriter.close();
    }
}
