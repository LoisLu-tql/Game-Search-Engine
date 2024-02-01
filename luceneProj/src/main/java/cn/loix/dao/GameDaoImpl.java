package cn.loix.dao;

import cn.loix.pojo.Game;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class GameDaoImpl implements GameDao {
    @Override
    public List<Game> queryGameList() {
        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;

        List<Game> list = new ArrayList<Game>();

        try{
            Class.forName("com.mysql.jdbc.Driver");
            connection = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/games_db", "root", "290102");

            String sql = "select * from games";

            preparedStatement = connection.prepareStatement(sql);
            resultSet = preparedStatement.executeQuery();

            while(resultSet.next()){
                Game game = new Game();
                game.setId(resultSet.getInt("id"));
                game.setGame_birth(resultSet.getString("game_birth"));
                game.setGame_developer(resultSet.getString("game_developer"));
                game.setGame_img(resultSet.getString("game_img"));
                game.setGame_intro(resultSet.getString("game_intro"));
                game.setGame_link(resultSet.getString("game_link"));
                game.setGame_name(resultSet.getString("game_name"));
                game.setGame_publisher(resultSet.getString("game_publisher"));
                game.setGame_src(resultSet.getString("game_src"));
                game.setGame_tag(resultSet.getString("game_tag"));
                list.add(game);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return list;
    }
}
