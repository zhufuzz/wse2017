package Retriever;

import java.io.*;
import java.net.URL;
import java.net.URLEncoder;
import java.util.List;
import java.util.ArrayList;
import java.net.URLEncoder;
import java.io.UnsupportedEncodingException;

/**
 * Created by Wenzhao on 4/22/16.
 */
public class Page {
    private String id;
    private double pageRank;
    private String content = null;
    private String lowerContent = null;
    private String url;
    private String title;
    private double dependencyScore = 0;
    private double totalScore;
    private int length;
    private String preview = " ";
    private int previewTokenSize = 0;
    private String scoreInfo = "";
    private boolean valid = false;
    private String pagePath;
    private int match = -1;
    private boolean titleContains = false;
    private boolean seen = false;
    private List<Sequence> currentSeq =
            new ArrayList<Sequence>();

    public Page(String id, double pageRank, String path) {
        this.id = id;
        this.pageRank = pageRank;
        pagePath = path;
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }

    @Override
    public String toString() {
        return title + "\n" + url + "\n" + preview + "\n";
    }

    public String getPreview() { return preview;}

    public String getID() {
        return id;
    }

    public String getUrl() {
        return url;
    }

    public String getTitle() {
        return title;
    }

    public double getPageRank() {
        return pageRank;
    }

    public int getMatch() {
        return match;
    }

    public String getPreview() {
        return preview;
    }

    /**
     * ADDED BY BIN LI
     * Convert page info to JSON format string.
     */
    public String toJSONResult() {
        StringBuilder pageJSON = new StringBuilder();
        pageJSON.append("{\"id\": ");
        pageJSON.append("\"");
        pageJSON.append(getID());
        pageJSON.append("\"");
        pageJSON.append(", \"title\": ");
        try {
            pageJSON.append("\"").append(URLEncoder.encode(getTitle(), "UTF-8")).append("\"");
        } catch (UnsupportedEncodingException e) {
            pageJSON.append("null");
        }
        pageJSON.append(", \"url\": \"").append(getUrl())
                .append("\", \"preview\": ");
        try {
            pageJSON.append("\"").append(URLEncoder.encode(getPreview(), "UTF-8"))
                    .append("\"");
        } catch (UnsupportedEncodingException e) {
            pageJSON.append("null");
        }
        pageJSON.append("}");

        return pageJSON.toString();
    }

    /**
     * This method prints out the score calculation history, for debug purpose
     */
    public String getScoreInfo() {
        return scoreInfo + "Dependency Score=" + dependencyScore + " pageRank=" + pageRank +
                " total=" + totalScore + "\n";
    }

    public boolean titleContains() {
        return titleContains;
    }

    /**
     * This method calculates the score based on the given sequence (because the same page will
     * have different scores for different sequences (i.e. word combination))
     */
    public void calculateScore() {
        for (Sequence seq: currentSeq) {
            double wordWeight = Retriever.getWeight(seq);
            String token = seq.getToken();
            int size = seq.getRight() - seq.getLeft() + 1;
            int titleCount = getCount(token.toLowerCase(), title.toLowerCase());
            if (titleCount != 0) {
                setMatch(size);
                setTitleContains(true);
            }
            int lowerCount = getCount(token.toLowerCase(), lowerContent);
            if (lowerCount == 0) {
//            scoreInfo += "Token: " + token + " Original=0 Lower=0 WordWeight=" + wordWeight + " wordTotal=0\n";
                continue;
            }
            int originalCount = getCount(token, content);
            lowerCount = lowerCount - originalCount;
            if (lowerCount != 0 || originalCount != 0) {
                setMatch(size);
            }
            double originalScore = formula(wordWeight, originalCount);
            double lowerScore = formula(wordWeight, lowerCount);
            final double weight = 1.5;
            double addedScore = weight * originalScore + lowerScore;
//        scoreInfo += "Token: " + token + " Original=" + originalScore + " Lower=" + lowerScore +
//                 " WordWeight=" + wordWeight + " wordTotal=" + addedScore + "\n";
            dependencyScore += addedScore;
        }
        currentSeq.clear();
    }

    public double finalScore() {
//        final double weight = 0;
//        totalScore = dependencyScore + weight * pageRank;
//        return totalScore;
        return dependencyScore;
    }

    /**
     * test if the page has complete information, incomplete pages will be discarded
     */
    public boolean isValid() {
        return valid;
    }

    public void setValid(boolean valid) {
        this.valid = valid;
    }

    /**
     * test if the page has been seen, to avoid duplicate parsing
     */
    public boolean isSeen() {
        return seen;
    }

    public void addSeq(Sequence seq) {
        currentSeq.add(seq);
    }

    public boolean isSeqEmpty() {
        return currentSeq.isEmpty();
    }

    /**
     * Parse the page file and store all useful information, please see
     * the structure of a page file for details
     */
    public void parsePage() {
        seen = true;
        int first = id.indexOf('_', 0);
        int second = id.indexOf('_', first + 1);
        String firstDir = "result_" + id.substring(0, first);
        String secondDir = id.substring(0, second);
        String fileName = id + ".page";
        String wholePath = pagePath + firstDir + File.separator + secondDir
                + File.separator + fileName;
        try {
            BufferedReader reader = new BufferedReader(new FileReader(wholePath));
            String line = null;
            while((line = reader.readLine()) != null) {
                if (line.equals("#ThisURL#")) {
                    url = reader.readLine();
                }
//                else if (line.equals("#Length#")) {
//                    length = Integer.parseInt(reader.readLine());
//                }
                else if (line.equals("#Title#")) {
                    title = reader.readLine();
                }
                else if (line.equals("#Content#")) {
                    content = reader.readLine();
                    lowerContent = content.toLowerCase();
                    break;
                }
            }
            reader.close();
            if (content == null) {
                return;
            }
            valid = true;
        } catch (IOException e) {
//            System.out.println("Parse page " + id + " not successful");
        }
    }

    /**
     * Count the number of occurrences of a token among the contents of the page,
     * in order to calculate dependency score later
     */
    private int getCount(String token, String content) {
        int index = 0;
        int count = 0;
//        String[] parts = token.split("\\s+");
//        int size = parts.length;
        boolean hasPreview = false;
        while ((index = content.indexOf(token, index)) != -1) {
            if (!hasPreview) {
                int end = Math.min(content.length(), index + 200);
                while (end < content.length() && content.charAt(end) != ' ') {
                    end++;
                }
                preview = content.substring(index, end);
                hasPreview = true;
            }
            count++;
            index += token.length();
        }
        return count;
    }

    private void setMatch(int match) {
        this.match = match;
    }

    private void setTitleContains(boolean titleContains) {
        this.titleContains = titleContains;
    }

    private double formula(double wordWeight, int count) {
        if (count == 0) {
            return 0;
        }
        double score = 1 + Math.log(count) / Math.log(2);
        return score * wordWeight;
    }
}
