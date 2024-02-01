package cn.loix.pojo;

import java.util.List;

public class SearchResults {
    private List<Game> gameList;
    private long total_count;
    private long page_count;
    private long page_now;
    private long search_time;
    private long page_time;
    private String search_way;

    public String getSearch_way() {
        return search_way;
    }

    public void setSearch_way(String search_way) {
        this.search_way = search_way;
    }

    public long getPage_time() {
        return page_time;
    }

    public void setPage_time(long page_time) {
        this.page_time = page_time;
    }

    public long getSearch_time() {
        return search_time;
    }

    public void setSearch_time(long search_time) {
        this.search_time = search_time;
    }

    public List<Game> getGameList() {
        return gameList;
    }

    public void setGameList(List<Game> gameList) {
        this.gameList = gameList;
    }

    public long getTotal_count() {
        return total_count;
    }

    public void setTotal_count(long total_count) {
        this.total_count = total_count;
    }

    public long getPage_count() {
        return page_count;
    }

    public void setPage_count(long page_count) {
        this.page_count = page_count;
    }

    public long getPage_now() {
        return page_now;
    }

    public void setPage_now(long page_now) {
        this.page_now = page_now;
    }
}
