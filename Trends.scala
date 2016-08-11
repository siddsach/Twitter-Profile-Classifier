package services
import integration.TwitterApp

import scala.collection.immutable.ListMap
import scala.collection.mutable
import scala.concurrent.ExecutionContext.Implicits.global
import org.apache.commons.io.filefilter.FalseFileFilter

import scala.concurrent.Future

/*Let's say we have an input list of handles from the D2 saved. We want to find out which current trends on twitter are these
people talking about. This will involve 1, pulling current trends on twitter, 2, pulling timelines, 3, creating a dictionary with each trend as a key, calculating the score of each tweet containing
each of those hashtags, adding that score to some constant for each mention, and adding each value to the
dictionary for that topic. In the end, we'll have the topics that are most popular in this community that
are trending right now.
 */

/* given that we have a list of posts for a profile, let's calculate the score
* */

//case class Tweet(text: String, hashtags: List[String], likes: Int, replies: Int, retweets: Int, comments: Int)

object Trends {
  /*we will weight mentions of topics by the following formula:
w = a + b * likes + c * replies + d * retweets + e * comments
TENTATIVE WEIGHTS: */
  val a = 10
  val b = 5
  val c = 2

  def calc(tweet: integration.TweetAPI, trend: String): Int = {
    if (tweet.text contains trend) {
      (b + c * tweet.retweet_count)
    } else {
      0
    }
  }

  def processTimeline(timeline: List[integration.TweetAPI], trend_dict: mutable.Map[String, Int]) = {
    trend_dict.map {
      case (trend, score) =>

        val t = timeline.map { tweet =>
          calc(tweet, trend)
        }
        var sumThing = if (t.isEmpty) {
          0
        } else {
          if (t.sum != 0) {
            val s = a + t.sum
            if ((s) >= 40) {
              40
            } else { s }
          } else { 0 }
        }

        trend_dict(trend) += sumThing
    }
  }

  def getNetworkTrends(handles: List[String], count: Int) = {
    var hashtags = mutable.Map[String, Int]()
    val t = TwitterApp.getTrends()
    t.map { list =>
      val a = list(0).trends
      a.map { trend => hashtags += trend.name -> 0 }

      val ftr = handles.map { username =>
        TwitterApp.getTimelineAPI(username, 200).map { timeline =>
          println(timeline)
          processTimeline(timeline, hashtags)
        }
      }

      Future.sequence(ftr).map { xx =>
        val a = ListMap(hashtags.toSeq.sortWith(_._2 > _._2): _*).toList
        val (left, right) = a.splitAt(count);
        println(left); left
      }

    }
  }

}

